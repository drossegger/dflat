from misc.ConfigParser import ConfigParser
from misc.Containers import Instance
from multiprocessing import Event
from output.TextWriter import LBWriter
import time,subprocess
import misc.util
import sys

class RunTest:
	def __init__(self, dflat, instances,portfolios,maxtime=600):
		self.dflat=dflat
		self.instances=instances
		self.portfolios=portfolios
		self.maxtime=maxtime
	


		
	def _printError(output):
		sys.stderr.write("%s, %s %s"%(self.instance.program,self.instance.instance,output))
		

	def run(self):
		count=0	
		lbwriter=LBWriter('learningbase.csv')
		for instance in self.instances:
			count+=1
			times=[]
			exitcodes=[]
			print "Instance %s/%s"%(count,len(self.instances))
			for portfolio in self.portfolios:
				program=misc.util.buildProgramString(self.dflat,instance,' --portfolio '+portfolio+' ')
				timestart=time.clock()
				call=subprocess.Popen(program,
						shell=True,
						stdout=subprocess.PIPE,
						stderr=subprocess.STDOUT)
				while call.poll() is None:
					if time.clock()-timestart > self.maxtime :
						call.kill()
						times.append((portfolio,-100))
				timeend=time.clock()
				call.poll()
				exitcodes.append((portfolio, call.returncode))
				if (timeend-timestart) < self.maxtime:
					times.append((portfolio,timeend-timestart))
			instance.runtimes=times
			instance.exitcodes=exitcodes
			lbwriter.write([instance])
			
			
		return self.instances


	

