import os
import random
import datetime as dt
import math
import numpy

consumptionData = None
consumptionDistribution = None
productionData = None
productionDistribution = None


#state consists of: charge in battery, consumption this hour, production this hour, time period of year
class State(object):
	def __init__(self, charge, consumption, production, time):
		self.charge = charge
		self.consumption = consumption
		self.production = production
		self.time = time

	#question about amount to sell - I presume that comes out of charge
    #pass in 0's for entries that aren't corresponding to an action, and a value for an action that you wish to take
	def reward(self, amountToCharge, amountToDischarge):
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
		return -1 * (price * netUsage)

#Returns history of stdDeviations from mean, and guess of (mean, stdDev) for next day
def getTransitionProbabilitiesForConsumption(state, history=None):
	global consumptionDistribution, consumptionData
	if state.time == (365*24):
		return -1
	if consumptionDistribution == None:
		consumptionData = readConsumptionByDate()
		consumptionDistribution = convertToDistribution(consumptionData)
	prevMean, prevStdDev = consumptionDistribution[state.time]
	distanceFromMean = (state.consumption - prevMean) / prevStdDev
	nextMean, nextStdDev = consumptionDistribution[state.time+1]
	if not history:		
		return [distanceFromMean], (nextMean + distanceFromMean * nextStdDev, nextStdDev)
	else:
		history.append(distanceFromMean)
		meanOfDistancesFromMean, standardDeviation = getMeanAndSampleDeviationOfSample(history)
		return history, (meanOfDistancesFromMean * nextStdDev + nextMean, standardDeviation)

def getTransitionProbabilitiesForProduction(state, history=None):
	global productionData, productionDistribution
	if state.time == (365*24):
		return -1
	if productionDistribution == None:
		productionData = readProductionByDate()
		productionDistribution = convertToDistribution(productionData)
	prevMean, prevStdDev = productionDistribution[state.time]
	distanceFromMean = (state.production - prevMean) / prevStdDev
	nextMean, nextStdDev = productionDistribution[state.time+1]
	if not history:		
		return [distanceFromMean], (nextMean + distanceFromMean * nextStdDev, nextStdDev)
	else:
		history.append(distanceFromMean)
		meanOfDistancesFromMean, standardDeviation = getMeanAndSampleDeviationOfSample(history)
		return history, (meanOfDistancesFromMean * nextStdDev + nextMean, standardDeviation)

#Below this is filereading/utility functions, feel free to ignore

def getMeanAndSampleDeviationOfSample(sample):
	mean = numpy.mean(sample)
	standardDeviation = numpy.std(sample)
	return mean, standardDeviation	

def readConsumptionByDate():
	data = []
	for i in range(365 * 24):
		data.append([])
	for filename in os.listdir("data/cleaned_data/consumption"):
		with open("data/cleaned_data/consumption/"+filename) as file: 
			i = 0
			for line in file:
				data[i].append(float(line))
				i += 1
	return data

def readProductionByDate():
	data = []
	for i in range(365 * 24):
		data.append([])
	for filename in os.listdir("data/cleaned_data/production"):
		with open("data/cleaned_data/production/"+filename) as file: 
			i = 0
			for line in file:
				data[i].append(float(line))
				i += 1
	return data


def convertToDistribution(data):
	distribution = []
	for i, times in enumerate(data):
		mean, stdDev = getMeanAndSampleDeviationOfSample(times)
		distribution.append((mean, stdDev))
	print distribution[0]
	return distribution
