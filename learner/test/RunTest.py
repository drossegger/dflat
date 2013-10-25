from misc.ConfigParser import ConfigParser
from misc.Containers import Instance
import misc.util
from timeit import Timer

class RunTest:
	def __init__(self, dflat, instances,portfolios):
		self.dflat=dflat
		self.instances=instances
		self.portfolios=portfolios
	
	def run(self):
		for instance in self.instances:
			times=[]
			for portfolio in self.portfolios:
				program=misc.util.buildProgramString(self.dflat,instance,' --portfolio '+portfolio+' ')
				t=Timer('subprocess.call("%s",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)' % program, setup='import subprocess')
				times.append((portfolio,min(t.repeat(repeat=1,number=1))))
			instance.runtimes=times
		return self.instances


	

