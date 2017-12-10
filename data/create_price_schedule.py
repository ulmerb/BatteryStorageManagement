import csv

def create_schedule(filename):
  
  f = open(filename, 'wb')
  writer = csv.writer(f)

  # price per kilowatt-hour for each hour of day
  daily_schedule = [0.07, 0.07, 0.08, 0.08, 0.09, 0.09, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, \
                    0.14, 0.15, 0.15, 0.16, 0.16, 0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.08]
  # convert to price per watt-hour
  daily_schedule = [p / 1000. for p in daily_schedule]
  
  num_hours_in_year = 8760

  for i in range(num_hours_in_year):
    writer.writerow([daily_schedule[i % 24]])

if __name__ == '__main__':
  filename = 'cleaned_data/price/simple_daily_schedule_new.csv'
  create_schedule(filename)
