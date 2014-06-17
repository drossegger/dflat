import numpy as np
import ast
class TextReader:
	def __init__(self,path):
		self.path=path
	def read(self):
		f=open(self.path)
		x=f.read()
		f.close()
		return x

class LBReader(TextReader):
	def read(self):
		f=open(self.path)
		i=f.read()
		f.close()
		instances=i.splitlines()
		instances=[a.split(';') for a in instances]
		instancetable=self._buildfirstline(instances[0])
		size=instancetable.shape[0]
		for instance in instances:
			row=np.array([instance[0],instance[1]])
			row=np.append(row,self._convertFeatures(instance[2]))
			row=np.append(row,self._convertPortfolios(instance[3]))
			instancetable=np.vstack((instancetable, row[0:size]))
		return instancetable
		





	def _convertPortfolios(self,portfolios):
		portfolios=ast.literal_eval('({0})'.format(portfolios))
		a=np.array([])
		for portfolio in portfolios:
			if portfolio[1]=='real':
				a=np.append(a,portfolio[2])
		return a
	def _convertFeatures(self,features):
		features=ast.literal_eval('({0})'.format(features))
		a=np.array([])
		for feature in features:
			if feature[0]=='dw':
				a=np.append(a,feature[1])
			else:
				a=np.append(a,feature[0])
		return a
	def _buildfirstline(self,firstline):
		a=np.array(['',''])
		features=ast.literal_eval('({0})'.format(firstline[2]))
		for feature in features:
				a=np.append(a,feature[1])
		portfolios=ast.literal_eval('({0})'.format(firstline[3]))
		for portfolio in portfolios:
			if portfolio[1]=='real':
				a=np.append(a,portfolio[0])
		return a

class InstanceReader(TextReader):
	def read(self):
		f=open(self.path)
		x=f.read()
		x=x.splitlines()
		x=[a.split(";") for a in x]
		return x

