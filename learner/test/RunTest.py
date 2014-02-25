from input.ConfigParser import ConfigParser
from base.Containers import Instance
from multiprocessing import Event
from output.TextWriter import LBWriter
import time,subprocess
import base.util
import sys

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
		
	def prepare(self):
		#print 'ulimit -v %s'%self.memout
		subprocess.Popen('ulimit -m %s'%self.memout,shell=True)
		subprocess.Popen('ulimit -v %s'%self.memout,shell=True) 
		subprocess.Popen('ulimit -H -m %s'%self.memout,shell=True)
		subprocess.Popen('ulimit -H -v %s'%self.memout,shell=True)

	def run(self):
		self.prepare()
		count=0	
		lbwriter=LBWriter(self.outputfile)
		for instance in self.instances:
			count+=1
			times=[]
			exitcodes=[]
			print "Instance %s/%s"%(count,len(self.instances))
			for portfolio in self.portfolios:
				program=base.util.buildProgramString(self.dflat,instance,' --portfolio '+portfolio+' ')
				timestart=time.clock()
				call=subprocess.Popen(program,
						shell=True,
						stdout=subprocess.PIPE,
						stderr=subprocess.STDOUT)
				while call.poll() is None:
					if time.clock()-timestart > self.maxtime :
						call.terminate()
						time.sleep(5)
						call.kill()
						#implement sleep 5 and then force kill (9)
						call.poll()
						if call.returncode==127 :
							times.append((portfolio,-50))
						else :
							times.append((portfolio,-100))
				
				timeend=time.clock()
				call.poll()
				
				exitcodes.append((portfolio, call.returncode))
				if (timeend-timestart) < self.maxtime:
					if call.returncode==127 :
						times.append((portfolio,-50))
					else :
						times.append((portfolio,timeend-timestart))

			instance.runtimes=times
			instance.exitcodes=exitcodes
			lbwriter.write([instance])
			
			
		return self.instances


	

