import csv
import os

def clean(filename):
  months = [str(i) for i in range(1, 13)]

  raw_file = open('raw_data/production/' + filename, 'rU')
  reader = csv.reader(raw_file)

  cleaned_file = open('cleaned_data/production/' + filename, 'wb')
  writer = csv.writer(cleaned_file)

  for row in reader:
    if not row[0] in months:
      continue

    writer.writerow([row[-1]])

  raw_file.close()
  cleaned_file.close()

if __name__ == '__main__':
  for filename in os.listdir('raw_data/production'):
    clean(filename)

