import numpy as np
import cvxpy
import sys
import time

hours_in_year = 8760
hours_in_day = 24

def calculate_reward(price, consumption, production, discharge):
  return price * (consumption - production - discharge)

def sample_normal(history_data):
  if len(history_data) == 1:
    return history_data[0]
  else:
    mu = np.mean(history_data)
    sigma = np.std(history_data)
    return np.random.normal(loc=mu, scale=sigma)

def draw_state_samples(production_history_per_hour,
                       consumption_history_per_hour,
                       price_history_per_hour,
                       depth,
                       current_hour):

  sampled_production = []
  sampled_consumption = []
  sampled_price = []

  for d in range(depth):
    hour = (current_hour + d + 1) % hours_in_day

    production_history = production_history_per_hour[hour]
    consumption_history = consumption_history_per_hour[hour]
    price_history = price_history_per_hour[hour]

    if len(production_history) == 0 or len(consumption_history) == 0 or len(price_history) == 0:
      break

    production_sample = sample_normal(production_history)
    consumption_sample = sample_normal(consumption_history)
    price_sample = sample_normal(price_history)

    sampled_production.append(production_sample)
    sampled_consumption.append(consumption_sample)
    sampled_price.append(price_sample)

  return sampled_production, sampled_consumption, sampled_price
        
def run_linear_program(production,
                       consumption,
                       price,
                       initial_battery_level,
                       battery_size,
                       max_discharge_rate,
                       max_charge_rate):

  num_hours = len(production)

  battery_level = cvxpy.Variable(num_hours)
  battery_discharge = cvxpy.Variable(num_hours)

  constraints = []
  constraints += [battery_level[0] == initial_battery_level]
  constraints += [battery_level >= 0.]
  constraints += [battery_level <= battery_size]

  for t in range(1, num_hours):
    constraints += [battery_level[t] == battery_level[t-1] - battery_discharge[t-1]]

  constraints += [battery_discharge <= max_discharge_rate]
  constraints += [battery_discharge >= -max_charge_rate]

  _production = np.array(production)
  _consumption = np.array(consumption)
  _price = np.array(price)

  objective = cvxpy.Minimize(_price * (_consumption - _production - battery_discharge))

  problem = cvxpy.Problem(objective, constraints)
  problem.solve(solver='GLPK', verbose=False)

  return battery_discharge.value

def online_algorithm(production_filename,
                     consumption_filename,
                     price_filename,
                     battery_size,
                     max_discharge_rate,
                     max_charge_rate):
  
  num_samples = 25
  depth = 12

  production = np.genfromtxt(production_filename)
  consumption = np.genfromtxt(consumption_filename)
  price = np.genfromtxt(price_filename)
  
  battery_levels = []
  battery_discharges = []
  total_cost = 0.

  production_history_per_hour = [[] for _ in range(hours_in_day)]
  consumption_history_per_hour = [[] for _ in range(hours_in_day)]
  price_history_per_hour = [[] for _ in range(hours_in_day)]

  battery_level = 0.

  for h in range(hours_in_year):
    print h
    hour_of_day = h % hours_in_day

    battery_levels.append(battery_level)

    observed_production = production[h]
    observed_consumption = consumption[h]
    observed_price = price[h]

    production_history_per_hour[hour_of_day].append(observed_production)
    consumption_history_per_hour[hour_of_day].append(observed_consumption)
    price_history_per_hour[hour_of_day].append(observed_price)

    sampled_actions = []
    
    s = time.time()
    for _ in range(num_samples):
      
      sampled_production, sampled_consumption, sampled_price = draw_state_samples(production_history_per_hour,
                                                                                  consumption_history_per_hour,
                                                                                  price_history_per_hour,
                                                                                  depth,
                                                                                  hour_of_day)

      if len(sampled_production) == 0 or len(sampled_consumption) == 0 or len(sampled_price) == 0:
        sampled_actions.append(0.)
      else:
        production_s = [observed_production] + sampled_production
        consumption_s = [observed_consumption] + sampled_consumption
        price_s = [observed_price] + sampled_price

        actions = run_linear_program(production_s,
                                     consumption_s,
                                     price_s,
                                     battery_level,
                                     battery_size,
                                     max_discharge_rate,
                                     max_charge_rate)

        sampled_actions.append(actions[0])
    
    print time.time() - s
    discharge = np.mean(sampled_actions)
    battery_level = battery_level - discharge
    battery_discharges.append(discharge)
    cost = observed_price * (observed_consumption - observed_production - discharge)
    total_cost += cost
    
  return battery_levels, battery_discharges, total_cost


if __name__ == '__main__':
  if len(sys.argv) < 4:
    print 'need 3 arguments for production, consumption, price data'
  else:
    production_filename = sys.argv[1]
    consumption_filename = sys.argv[2]
    price_filename = sys.argv[3]

    battery_size = 40. * 1000
    max_discharge_rate = 20. * 1000
    max_charge_rate = 20. * 1000

    battery_levels, battery_discharges, total_cost = online_algorithm(production_filename,
                                                                      consumption_filename,
                                                                      price_filename,
                                                                      battery_size,
                                                                      max_discharge_rate,
                                                                      max_charge_rate)
    print total_cost
    
