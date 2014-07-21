import numpy as np
from sklearn import preprocessing

class Classifier:
	self.features
	self.labels
	def __init__(self,learningbase,features, runtimes):
		self.lb=learningbase
		self.runtimes=runtimes
		self.features=features	

	def prepare(self):
		for runtime in runtimes:
			self.labels.append(_label(runtime))


	def _label(self,runtimes):
		runtimes=[float(x) for x in runtimes]
		label=1
		if len(set(runtimes)) == 1:
			if runtimes[0]<0:
				label=0
			else:
				label=6
		else:
			for i in range(5):
				if runtimes[i] > 100 and runtimes[i] < runtimes[label-1]:
					label=i+1
		return label


class SVMClassifier(Classifier):

