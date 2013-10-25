import xml.etree.ElementTree as ET
import sys
from Containers import Instance 

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
		for xmlInstance in xmlInstances.iter('instance'):
			instance=Instance()
			for edge in xmlInstance.iter('edge'):
				instance.edges.append(edge.text)
			mlvl=xmlInstance.find('multi-level')
			if mlvl != None:
				instance.multilevel=True
			exch=xmlInstance.find('exchange-program')
			if exch != None:
				instance.exchprogram=exch.text
			joinprogram=xmlInstance.find('join-program').text
			if joinprogram==None:
				print('ERROR in config.xml: Missing join-program in instance')
				sys.exit(1)
			instance.joinprogram=joinprogram 
			inputfile=xmlInstance.find('input-file').text 
			if inputfile==None: 
				print('ERROR in config.xml: Missing input-file in instance')
				sys.exit(1)
			instance.inputfile=inputfile
			self.instances.append(instance)
	






