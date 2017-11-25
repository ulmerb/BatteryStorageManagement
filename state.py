import os
import random
import datetime as dt
import math

consumptionData = None
consumptionDistribution = None

#state consists of: charge in battery, consumption this hour, production this hour, time of day, day of year
class State(object):
	def __init__(self, charge, consumption, production, time, day):
		self.charge = charge
		self.consumption = consumption
		self.production = production
		self.time = time
		self.day = day

	#question about amount to sell - I presume that comes out of charge
    #pass in 0's for entries that aren't corresponding to an action, and a value for an action that you wish to take
	def reward(self, amountToSell, amountToCharge, amountToDischarge):
		price = 0
		if self.time < 9 or self.time >= 22:
			price = .212
		elif self.time <= 12 or self.time >= 18:
			price = .239
		else:
			price = .263
		if amountToDischarge > self.charge or amountToSell > self.charge or amountToCharge > self.production:
			return -float("inf")
		netUsage = self.consumption - self.production - amountToCharge + amountToDischarge
		return -1 * (price * netUsage) + price * amountToSell

#Returns history of stdDeviations from mean, and guess of (mean, stdDev) for next day
def getTransitionProbabilitiesForConsumption(state, history=None):
	global consumptionDistribution, consumptionData
	if state.day == 365:
		return -1
	if consumptionDistribution == None:
		consumptionData = readConsumptionByDate()
		consumptionDistribution = convertToDistribution(consumptionData)
	prevMean, prevStdDev = consumptionDistribution[state.day][state.time]
	distanceFromMean = (state.consumption - prevMean) / prevStdDev
	nextMean = 0
	nextStdDev = 0
	if state.time == 24:
		nextMean, nextStdDev = consumptionDistribution[state.day+1][0]
	else:
		nextMean, nextStdDev = consumptionDistribution[state.day][state.time + 1]
	if not history:		
		return [distanceFromMean], (nextMean + distanceFromMean * nextStdDev, nextStdDev)
	else:
		history.append(distanceFromMean)
		meanOfDistancesFromMean, standardDeviation = getMeanAndSampleDeviationOfSample(history)
		return history, (meanOfDistancesFromMean * nextStdDev + nextMean, standardDeviation)



#Below this is filereading/utility functions, feel free to ignore

def isInteger(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def readConsumptionByBuilding():
	data = []
	for filename in os.listdir("data/consumption"):
		with open("data/consumption/"+filename) as file: 
			yearData = []
			for i in range(365):
				hours = [0] * 24
				yearData.append(hours)
			for line in file:
				line = line.strip().split()
				date = line[0].split("/")
				if not isInteger(date[0]):
					continue
				month = int(date[0])
				day = int(date[1])
				day = (dt.date(2017, month, day) - dt.date(2017,1,1)).days + 1
				usage = line[1].split(",")
				hour = int(usage[0][:2])
				electricityUsage = 0
				for i in range(len(usage)-1):
					electricityUsage += float(usage[i+1])
				yearData[day-1][hour-1] = electricityUsage
			data.append(yearData)
	return data

def getMeanAndSampleDeviationOfSample(sample):
	mean = 0
	for value in sample:
		mean += value
	mean /= len(sample)
	standardDeviation = 0
	for value in sample:
		standardDeviation += (value - mean) ** 2
	standardDeviation /= len(sample)
	return mean, standardDeviation	

def readConsumptionByDate():
	data = []
	for i in range(365):
		hours = [None] * 24
		data.append(hours)
	for filename in os.listdir("data/consumption"):
		with open("data/consumption/"+filename) as file: 
			for line in file:
				line = line.strip().split()
				date = line[0].split("/")
				if not isInteger(date[0]):
					continue
				month = int(date[0])
				day = int(date[1])
				day = (dt.date(2017, month, day) - dt.date(2017,1,1)).days + 1
				usage = line[1].split(",")
				hour = int(usage[0][:2])
				electricityUsage = 0
				for i in range(len(usage)-1):
					electricityUsage += float(usage[i+1])
				if data[day-1][hour-1] == None:
					data[day-1][hour-1] = []
				data[day-1][hour-1].append(electricityUsage)
	return data

def readProductionByDate():
	data = []
	for i in range(365):
		hours = [None] * 24
		data.append(hours)
	for filename in os.listdir("data/production"):
		with open("data/production/"+filename) as file: 
			for line in file:
				line = line.strip().split()
				valid = True
				line = line.strip().split()


def convertToDistribution(data):
	distribution = []
	for i in range(365):
		hours = [None] * 24
		distribution.append(hours)
	for i, day in enumerate(data):
		for j, hour in enumerate(day):
			expectation = 0
			squaredExpectation = 0
			values = 0
			valid = True
			for value in hour:
				if value == None:
					valid = False
					continue
				values += 1
				expectation += value
				squaredExpectation += value ** 2
			if not valid:
				continue
			expectation = expectation / values
			stdDev = math.sqrt(squaredExpectation / values - expectation ** 2)
			distribution[i][j] = (expectation, stdDev)
	return distribution

print getTransitionProbabilitiesForConsumption(State(1,1,1,1,1), [-55])