import xml.etree.ElementTree as ET
import sys,os
from base.Containers import Instance 

class ConfigParser:
	xmlfile='config.xml'
	tree = ET.parse('config.xml')
	root = tree.getroot()
	instances=[]

	def __init__(self):
		self.getFeatures() 
		self.getPortfolios() 
		self.getDFLATPath() 
		self.getInstances() 
		self.getGringoPath()
		self.getInstanceGroups()
	

	def getInstanceGroups(self):
	
		for group in self.root.iter('instance-group'):
			normalizations=[]	
			for normalization in group.findall('normalization'):
				normalizations.append((normalization.text,normalization.get('join-type')))
			program=group.find('program').text
			exchange=group.find('exchange').text
			mlvl=group.find('multi-level')
			inputfiledir=group.find('input-file-dir').text
			xmlInstances=os.listdir(inputfiledir)
			for xmlInstance in xmlInstances:
				for normalization in normalizations:
					instance=Instance()
					instance.exchange=exchange
					instance.program=program
					instance.inputfile=inputfiledir+xmlInstance
					instance.normalization=normalization[0]
					if normalization[1]=='default':
						instance.defjoin=True
					if mlvl != None:
						instance.multilevel=True
					for edge in group.iter('edge'):
						instance.edges.append(edge.text)
					self.instances.append(instance)



	def getGringoPath(self):
		self.gringo=self.root.find('gringo').text
	def getPortfolios(self): 
		self.portfolios = [portfolio.text for portfolio in self.root.iter('portfolio')] 

	def getFeatures(self): 
		xmlFeatures=self.root.find('features') 
		if(xmlFeatures != None): 
			self.features = [feature.attrib.get('name') for feature in xmlFeatures.iter('feature')] 
			
	def getDFLATPath(self): 
		self.dflat = self.root.find('dflat').text

	def getInstances(self):
		xmlInstances=self.root.find('instances')
		if xmlInstances!=None:
			for xmlInstance in xmlInstances.iter('instance'):
				instance=Instance()
				for edge in xmlInstance.iter('edge'):
					instance.edges.append(edge.text)
				mlvl=xmlInstance.find('multi-level')
				if mlvl != None:
					instance.multilevel=True
				program=xmlInstance.find('program').text
				if program==None:
					print('ERROR in config.xml: Missing join-program in instance')
					sys.exit(1)
				instance.program=program 
				inputfile=xmlInstance.find('input-file').text 
				if inputfile==None: 
					print('ERROR in config.xml: Missing input-file in instance')
					sys.exit(1)
				instance.inputfile=inputfile
				normalization=xmlInstance.find('normalization')
				if normalization==None:
					instance.normalization='none'
				else:
					instance.normalization=normalization.text
				defjoin=xmlInstance.find('default-join')
				if defjoin==None:
					instance.defjoin=False
				else:
					instance.defjoin=True
				heuristic=xmlInstance.find('elimination')
				if heuristic!=None:
					instance.heuristic=heuristic
				self.instances.append(instance)
	






