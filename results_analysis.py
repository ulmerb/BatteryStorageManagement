import pickle
import os
import matplotlib.pyplot as plt
import numpy as np

avg_lowend_impr = {20 : 0.0, 40 : 0.0, 80 : 0.0}
avg_highend_impr = {20 : 0.0, 40 : 0.0, 80 : 0.0}
avg_online_impr = {20 : 0.0, 40 : 0.0, 80 : 0.0}
count = 0

for filename in os.listdir('results'):
  count += 1
  if count != 2:
    continue
  print filename
  r = pickle.load(open('results/' + filename, 'rb'))
  print 'no battery'
  print r['no_battery_cost']
  print '40 kwh lowend'
  print r[40]['lowend']['cost']
  print '40 kwh highend'
  print r[40]['highend']['cost']
  print '40 kwh online'
  print r[40]['online']['cost']

  no_battery_cost = r['no_battery_cost']

  for battery_size in [20, 40, 80]:
    lowend_cost = r[battery_size]['lowend']['cost']
    highend_cost = r[battery_size]['highend']['cost']
    online_cost = r[battery_size]['online']['cost']
  
    lowend_abs_impr = no_battery_cost - lowend_cost
    highend_abs_impr = no_battery_cost - highend_cost
    online_abs_impr = no_battery_cost - online_cost

    lowend_impr = lowend_abs_impr / abs(no_battery_cost)
    highend_impr = highend_abs_impr / abs(no_battery_cost)
    online_impr = online_abs_impr / abs(no_battery_cost)

    avg_lowend_impr[battery_size] += lowend_impr
    avg_highend_impr[battery_size] += highend_impr
    avg_online_impr[battery_size] += online_impr

  prod_file, cons_file, price_file = filename.split(':')
  price_file = os.path.splitext(price_file)[0]
  print prod_file, cons_file, price_file


  g = np.genfromtxt('data/cleaned_data/production/' + prod_file + '.csv')
  c = np.genfromtxt('data/cleaned_data/consumption/' + cons_file + '.csv')
  p = np.genfromtxt('data/cleaned_data/price/' + price_file + '.csv')
  l = np.array(r[40]['online']['battery_level'])

  start_index = 200 * 24
  end_index = 203* 24
  h = range(start_index, end_index)

  fig, ax1 = plt.subplots()
  ax2 = ax1.twinx()
  g_label, = ax1.plot(h, 0.001 * g[start_index:end_index], 'g-')
  c_label, = ax1.plot(h, 0.001 * c[start_index:end_index], 'b-')
  l_label, = ax1.plot(h, 0.001 * l[start_index:end_index], 'y-')
  p_label, = ax2.plot(h, 1000 * p[start_index:end_index], 'r-')

  plt.legend((g_label, c_label, l_label, p_label), ('Production', 'Consumption', 'Battery Level', 'Price'))

  ax1.set_xlabel('hour')
  ax1.set_ylabel('kWh')
  ax2.set_ylabel('$/kWh')

  plt.show()


  plt.show()

#for battery_size in [20, 40, 80]:
#  avg_lowend_impr[battery_size] /= count
#  avg_highend_impr[battery_size] /= count
#  avg_online_impr[battery_size] /= count

print avg_lowend_impr
print avg_highend_impr
print avg_online_impr

