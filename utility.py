import matplotlib.pyplot as plt
import numpy as np

#Pass in data as an array of the points we want to plot
def createLineGraph(data):
	fig,ax = plt.subplots(1)

	x = np.array(data)
	y = np.arange(len(data))
	ax.plot(x,y)
	plt.show()