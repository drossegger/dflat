import subprocess, re, misc.util
from misc.ConfigParser import *
from misc.Containers import Instance

class FeatureExtractor:
	def __init__(self, dflat,instances):
		self.instances=instances
		self.dflat=dflat
		
	def extract(self):
		for instance in self.instances:
			instance.features=self.extractInstance(instance)
		return self.instances


	def extractInstance(self,instance):
		output = subprocess.check_output(misc.util.buildProgramString(self.dflat,instance,' --only-extract'),shell=True)
		result = re.compile(r'(.*\n)*begin features\n((.*\n)+)end features\n(.*\n)*',re.MULTILINE)
		lines = result.match(output).group(2).splitlines()
		lines = [x.split(';') for x in lines]
		return [(x[0],float(x[1])) for x in lines]

