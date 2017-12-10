# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os

#Pass in data as an array of the points we want to plot
def createLineGraph(data):
	fig,ax = plt.subplots(1)

	x = np.array(data)
	y = np.arange(len(data))
	ax.plot(x,y)
	plt.show()

sizes = [20,40,80]
algorithms = ['lowend','highend','online']
count = 0
averageCostsForTwenty = [0]*3
for filename in os.listdir('results/'):
	print filename
	f= open('results/'+filename, 'rb')
	result = pickle.load(f)
	count += 1
	for i, algorithm in enumerate(algorithms):
		averageCostsForTwenty[i] += result[20][algorithm]['cost']

for i, cost in enumerate(algorithms):
	averageCostsForTwenty[i] = float(averageCostsForTwenty[i])/ count
print averageCostsForTwenty
