import numpy as np
from sklearn import preprocessing
import pickle
from sklearn import svm

class Classifier:
	labels=[]
	scaler=None
	def __init__(self,config=None,features=None, runtimes=None):
		self.runtimes=runtimes
		self.features=features	
		self.config=config

	def prepare(self):
		for runtime in self.runtimes:
			self.labels.append(self._label(runtime))
		self.features=self._preprocess(self.features)

	def _preprocess(self,features):
		features=np.array(features)
		for f in self.config.features:
			if f.nominal==True:
				enc= preprocessing.OneHotEncoder()
				nF=self._txt2num(features[:,f.column])
				#if len(set(nF)) == 1:
				#	np.delete(self.features,f.column,1)
				#else:
				features[:,f.column]=nF #TODO
			else:
				nF=features[:,f.column]
				nF=[float(a) for a in nF]
				features[:,f.column]=nF
		enc=preprocessing.StandardScaler()
		features=enc.fit_transform(features)
		self.scaler=enc
		return features
	def _txt2num(self,feature):
		cat=list(set(feature))
		nF=[]
		for f in feature:
			for i in range(len(cat)):
				if cat[i]==f:
					nF.append(i)
		return nF
	def saveModel(self,path):
		pickle.dump(self,open(path,'wb'))
	def loadModel(self,path):
		return pickle.load(open(path,'rb'))

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
				if runtimes[i] > -100 and runtimes[i] < runtimes[label-1]:
					label=i+1
		return label


class SVMClassifier(Classifier):
	
	def buildModel(self):
		clf=svm.SVC()
		clf.fit(self.features,self.labels)
		self.clf=clf
	def predict(self, ifeat):
		i=[None]*len(self.config.features)
		ifeat=dict([(y,x) for (x,y) in ifeat])

		for f in self.config.features:
			if f.name=="dw": i[f.column]=float(ifeat.get("dw"))
			elif f.name=="heuristic": i[f.column]=float(ifeat.get("heuristic"))
			elif f.name=="nbredgepred": i[f.column]=float(ifeat.get("nbredgepred"))
			elif f.name=="nbredgefacts": i[f.column]=float(ifeat.get("nbredgefacts"))
			elif f.name=="gconstraints": i[f.column]=float(ifeat.get("gconstraints"))
			elif f.name=="gpredicates": i[f.column]=float(ifeat.get("gpredicates"))
			elif f.name=="gnontrivial": i[f.column]=float(ifeat.get("gnontrivial"))
			elif f.name=="gcomponents": i[f.column]=float(ifeat.get("gcomponents"))
			
		return self.clf.predict(self.scaler.transform(i))[0]




