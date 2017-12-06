import cvxpy
import numpy as np
import sys

def run_linear_program(production_filename,
                       consumption_filename,
                       price_filename,
                       battery_size,
                       max_discharge_rate,
                       max_charge_rate):

  # production[t] is the energy production in watt-hours at time t
  production = np.genfromtxt(production_filename)
  # consumption[t] is the energy consumption in watt-hours at time t
  consumption = np.genfromtxt(consumption_filename)
  # price[t] is the price of a watt-hour of energy in dollars at time t
  price = np.genfromtxt(price_filename)

  hours_in_year = 8760

  # battery_level[t] is the amount of energy contained in the battery in watt-hours at time t
  battery_level = cvxpy.Variable(8760)
  # battery_discharge[t] is the rate of discharge in watts at time t; this is positive if the battery is
  # discharging and negative if the battery is charging
  battery_discharge = cvxpy.Variable(8760)

  constraints = []
  # battery must start empty
  constraints += [battery_level[0] == 0.]
  # battery must always contain a non-negative amount of energy
  constraints += [battery_level >= 0.]
  # battery must not contain an amount of energy greater than its capacity
  constraints += [battery_level <= battery_size]

  # amount of energy contained in the battery at time t must always equal the amount of energy contained
  # in the battery at time t-1 minus the amount of discharged energy at time t-1
  for t in range(1, 8760):
    constraints += [battery_level[t] == battery_level[t - 1] - battery_discharge[t - 1]]

  # battery must not discharge at a rate greater than the maximum discharge rate
  constraints += [battery_discharge <= max_discharge_rate]
  # battery must not charge at a rate greater than the maximum charge rate (note that max_charge_rate is given
  # as a positive number)
  constraints += [battery_discharge >= -max_charge_rate]

  # cost at time t is the net energy bought from grid (consumption[t] - production[t] - battery_discharge[t]; this
  # is negative if energy is being sold back to the grid) times the price of energy at time t; the total cost is the
  # sum of these costs over all t
  objective = cvxpy.Minimize(price * (consumption - production - battery_discharge))

  problem = cvxpy.Problem(objective, constraints)
  problem.solve(solver = 'SCS', verbose = True)

  return battery_level.value, battery_discharge.value, problem.value


if __name__ == '__main__':
  if len(sys.argv) < 4:
    print 'need 3 arguments for production, consumption, price data'
  else:
    production_filename = sys.argv[1]
    consumption_filename = sys.argv[2]
    price_filename = sys.argv[3]

    # in watt-hours
    battery_size = 40. * 1000
    # in watts
    max_discharge_rate = 20. * 1000
    # in watts
    max_charge_rate = 20. * 1000

    battery_level, battery_discharge, total_cost = run_linear_program(production_filename,
                                                                        consumption_filename,
                                                                        price_filename,
                                                                        battery_size,
                                                                        max_discharge_rate,
                                                                        max_charge_rate)
    print total_cost
