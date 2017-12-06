import numpy as np
import csv
import sys

def low_end_baseline(production_filename,
                       consumption_filename,
                       price_filename,
                       battery_size,
                       max_discharge_rate,
                       max_charge_rate,
                       daily_charge_start_time,
                       daily_discharge_start_time):

  if (daily_charge_start_time == daily_discharge_start_time):
    print 'ERROR: Enter a daily_charge_start_time that is different than the daily_discharge_start_time'

  # production[t] is the energy production in watt-hours at time t
  production = np.genfromtxt(production_filename)
  # consumption[t] is the energy consumption in watt-hours at time t
  consumption = np.genfromtxt(consumption_filename)
  # price[t] is the price of a watt-hour of energy in dollars at time t
  price = np.genfromtxt(price_filename)

  max_charge_in_one_hour = max_charge_rate # assumed to be a positive value
  max_discharge_in_one_hour = max_discharge_rate #assumed to be a positive value

  hours_in_year = 8760
  hours_in_a_day = 24




  # battery_level[t] is the amount of energy contained in the battery in watt-hours at time t
  battery_level = np.zeros(hours_in_year) #pre-allocate as zeros.
  # battery_discharge[t] is the rate of discharge in watts at time t; this is positive if the battery is
  # discharging and negative if the battery is charging
  battery_discharge = np.zeros(hours_in_year) #pre-allocate as zeros.

  # Populate battery_discharge vector and battery_level vectors according to the low-end baseline strategy:
  # charge at max_charge_rate at 6am, and discharge at max_discharge_rate at 2pm everyday, making sure you stop charging either when you are
  # full or when it is 2pm. And don't charge when you're full, but that shouldn't ever happen with this policy. 

  for t in range(1,hours_in_year): 
    if (((t % hours_in_a_day) == daily_charge_start_time) | (battery_discharge[t - 1] == -max_charge_rate)) & (battery_level[t - 1] < (battery_size - max_charge_in_one_hour)) & ((t % hours_in_a_day) != daily_discharge_start_time):
      battery_discharge[t] = -max_charge_rate #Charge it only when: either you're at the daily charge time or at the last timestep you were charging AND if you are not at capacity
      # (note that max_charge_rate is given as a positive number)
    if (((t % hours_in_a_day) == daily_discharge_start_time) | (battery_discharge[t - 1] == max_discharge_rate)) & (battery_level[t - 1] > max_discharge_in_one_hour) & ((t % hours_in_a_day) != daily_charge_start_time):
      battery_discharge[t] = max_discharge_rate #discharge it only when its either at the daily discharge time or at the last timestep you were discharging AND if your are not empty, and if you are not at the daily charge time.
      #thus if the battery were unlimited in capacity. This would lead to constantly charging starting at the charge time, and then discharging at the discharge time until the next charge time. 

    # amount of energy contained in the battery at time t must always equal the amount of energy contained
    # in the battery at time t-1 minus the amount of discharged energy at time t-1
    battery_level[t] = battery_level[t - 1] - battery_discharge[t - 1]




  # cost at time t is the net energy bought from grid (consumption[t] - production[t] - battery_discharge[t]; this
  # is negative if energy is being sold back to the grid) times the price of energy at time t; the total cost is the
  # sum of these costs over all t
  cost = np.zeros(hours_in_year) # pre-allocate the cost vector
  cost = price * (consumption - production - battery_discharge)
  total_cost = np.sum(cost)

  # contraints it must abided by
  # battery must not charge more than its capacity
  # battery must not discharge past 0.  ... I could imagine a case where the battery has discharged close to zero, and then when I charge it. It messes up. 
  # battery must start empty
  # battery must always contain a non-negative amount of energy
  # battery must not contain an amount of energy greater than its capacity

  return battery_level, battery_discharge, total_cost


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

    daily_charge_start_time = 0 #12am in military time
    daily_discharge_start_time = 15 #3pm in military time

    battery_level, battery_discharge, total_cost = low_end_baseline(production_filename,
                                                                        consumption_filename,
                                                                        price_filename,
                                                                        battery_size,
                                                                        max_discharge_rate,
                                                                        max_charge_rate,
                                                                        daily_charge_start_time,
                                                                        daily_discharge_start_time)
    print total_cost
