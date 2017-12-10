from online import online_algorithm
from highend_baseline import run_linear_program
from lowend_baseline import low_end_baseline
from no_battery import no_battery
import pickle
import os


cities = ['losangeles', 'sanfrancisco', 'phoenix']
# in kwh
battery_sizes = [20., 40., 80.]
daily_charge_start_time = 0
daily_discharge_start_time = 15
max_discharge_rate = 20.
max_charge_rate = 20.

for city in cities:
  for production_filename in os.listdir('data/cleaned_data/production'):
    if not city in production_filename:
      continue

    for consumption_filename in os.listdir('data/cleaned_data/consumption'):
      if not city in consumption_filename:
        continue
      
      production = 'data/cleaned_data/production/' + production_filename
      consumption = 'data/cleaned_data/consumption/' + consumption_filename
      price = 'data/cleaned_data/price/simple_daily_schedule_new.csv'
      
      result = {}

      no_battery_cost = no_battery(production, consumption, price)

      result['no_battery_cost'] = no_battery_cost

      p_name = os.path.splitext(production_filename)[0]
      c_name = os.path.splitext(consumption_filename)[0]

      for battery_size in battery_sizes:
        lowend_battery_level, lowend_battery_discharge, lowend_cost = low_end_baseline(production, 
                                                                                       consumption,
                                                                                       price,
                                                                                       battery_size * 1000,
                                                                                       max_discharge_rate * 1000,
                                                                                       max_charge_rate * 1000,
                                                                                       daily_charge_start_time,
                                                                                       daily_discharge_start_time)
        highend_battery_level, highend_battery_discharge, highend_cost = run_linear_program(production,
                                                                                            consumption,
                                                                                            price,
                                                                                            battery_size * 1000,
                                                                                            max_discharge_rate * 1000,
                                                                                            max_charge_rate * 1000)
        online_battery_level, online_battery_discharge, online_cost = online_algorithm(production,
                                                                                       consumption,
                                                                                       price, 
                                                                                       battery_size * 1000,
                                                                                       max_discharge_rate * 1000,
                                                                                       max_charge_rate * 1000)

        result[battery_size] = {'lowend' : {'battery_level' : lowend_battery_level,
                                            'battery_discharge' : lowend_battery_discharge,
                                            'cost' : lowend_cost},
                                'highend' : {'battery_level' : highend_battery_level,
                                             'battery_discharge' : highend_battery_discharge,
                                             'cost' : highend_cost},
                                'online' : {'battery_level' : online_battery_level,
                                            'battery_discharge' : online_battery_discharge,
                                            'cost' : online_cost}}

      pickle.dump(result, open(p_name + ':' + c_name + ':simple_daily_schedule_new.p', 'wb')) 









