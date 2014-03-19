from input.ConfigParser import ConfigParser
from base.Containers import Instance
from multiprocessing import Event
from output.TextWriter import LBWriter
import time,subprocess
import base.util
import sys,resource

class RunTest:
	memout=16777216

	def __init__(self, dflat, instances,portfolios,maxtime=600,outputfile='learningbase.csv'):
		self.dflat=dflat
		self.instances=instances
		self.portfolios=portfolios
		self.maxtime=maxtime
		self.outputfile=outputfile
	


		
	def _printError(output):
		sys.stderr.write("%s, %s %s"%(self.instance.program,self.instance.instance,output))
		
	def _limit(self):
		resource.setrlimit(resource.RLIMIT_AS,(self.memout*1024,self.memout*1024))
		resource.setrlimit(resource.RLIMIT_RSS,(self.memout*1024,self.memout*1024))

	def run(self):
		count=0	
		lbwriter=LBWriter(self.outputfile)
		for instance in self.instances:
			count+=1
			times=[]
			exitcodes=[]
			print "Instance %s/%s"%(count,len(self.instances))
			for portfolio in self.portfolios:
				print portfolio
				program=base.util.buildProgramString(self.dflat,instance,['--portfolio',portfolio])
				timestart=time.clock()
				call=subprocess.Popen(program,
						stdin=open(instance.inputfile),
						stdout=subprocess.PIPE,
						stderr=subprocess.STDOUT,preexec_fn=self._limit)
				while True:
					if call.poll() is not None:
						break
					if time.clock()-timestart > self.maxtime :
						call.terminate()
						time.sleep(5)
						call.kill()
						#implement sleep 5 and then force kill (9)
						times.append((portfolio,-100))
					time.sleep(0.1)
				
				timeend=time.clock()
				#call.poll()
				
				exitcodes.append((portfolio, call.returncode))
				if (timeend-timestart) < self.maxtime:
					times.append((portfolio,timeend-timestart))

			instance.runtimes=times
			instance.exitcodes=exitcodes
			lbwriter.write([instance])
			
			
		return self.instances


	

