import csv
import os

def clean(filename):
  
  raw_file = open('raw_data/consumption/' + filename, 'rU')
  reader = csv.reader(raw_file)

  cleaned_file = open('cleaned_data/consumption/' + filename, 'wb')
  writer = csv.writer(cleaned_file)

  reader.next()

  for row in reader:
    writer.writerow([float(row[1]) * 1000])

  raw_file.close()
  cleaned_file.close()

if __name__ == '__main__':
  for filename in os.listdir('raw_data/consumption'):
    clean(filename)

