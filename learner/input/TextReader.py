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
	def __init__(self,path,features):
		self.path=path
		self.features=features
	def read(self):
		f=open(self.path)
		i=f.read()
		f.close()
		instances=i.splitlines()
		instances=[a.split(';') for a in instances]
		features=[]
		portfolios=[]
		tablestructure=self._buildTable(instances[0])
		for instance in instances:
			features.append(self._convertFeatures(instance[2]),tablestructure[0])
			portfolios.append(self._convertPortfolios(instance[3]),tablestructur[1])
		
		return [features,portfolios]
			
			

		#instancetable=self._buildfirstline(instances[0])
		#size=instancetable.shape[0]
		#for instance in instances:
		#	row=np.array([instance[0],instance[1]])
		#	row=np.append(row,self._convertFeatures(instance[2]))
		#	row=np.append(row,self._convertPortfolios(instance[3]))
		#	print row
		#	instancetable=np.vstack((instancetable, row[0:size]))
		#return instancetable
		





	def _convertPortfolios(self,portfolios,tableStructure):
		portfolios=ast.literal_eval('({0})'.format(portfolios))
		a=[None]*length(tableStructure)
		for portfolio in portfolios:
			if portfolio[1]=='real':
				for i in range(length(tableStructure)):
					if tableStructure[i]==portfolio[0]:
						a[i]=portfolio[2]
		return a
	def _convertFeatures(self,features,tableStructure):
		features=ast.literal_eval('({0})'.format(features))
		a=[None]*length(tableStructure)
		for feature in features:
			for i in range(length(tableStructure)):
				if feature[0]=='dw':
					if tableStructure[i]=='dw':
						a[i]=feature[1]
				else:
					if tableStructure[i]==feature[1]:
						a[i]=feature[0]
		return a
	def _buildTable(self,line):
		features=ast.literal_eval('({0})'.format(line[2]))
		portfolios=ast.literal_eval('({0})'.format(line[3]))
		
		fTable=[]
		pTable=[]
		for i in range(length(features)):
			if features[i][0]=='dw':
				fTable.append(features[i][0])
				for feature in self.features:
					if feature.name==features[i][0]:
						feature.column=i
			else:
				fTable.append(features[i][1])
				for feature in self.features:
					if feature.name==features[i][1]:
						feature.column=i
		for portfolio in portfolios:
			if portfolio[1]=='real':	
				pTable.append(portfolio[0])
		return (fTable,pTable)

			

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

