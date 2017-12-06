import numpy as np
import sys

def no_battery(production_filename,
               consumption_filename,
               price_filename):

  production = np.genfromtxt(production_filename)
  consumption = np.genfromtxt(consumption_filename)
  price = np.genfromtxt(price_filename)

  total_cost = np.dot(price, consumption - production)
  return total_cost

if __name__ == '__main__':
  if len(sys.argv) < 4:
    print 'need 3 arguments for production, consumption, price data'
  else:
    production_filename = sys.argv[1]
    consumption_filename = sys.argv[2]
    price_filename = sys.argv[3]

    cost = no_battery(production_filename, consumption_filename, price_filename)
    print cost
