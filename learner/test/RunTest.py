from output.TextWriter import LBWriter
import time,subprocess
import base.util
import sys,resource,os

class RunTest:
	memout=16777216

	def __init__(self, dflat, instances,portfolios,maxtime=2400,outputfile='learningbase.csv'):
		self.dflat=dflat
		self.instances=instances
		self.portfolios=portfolios
		self.maxtime=maxtime
		self.outputfile=outputfile
	


		
	def _printError(self,output):
		sys.stderr.write("%s, %s %s"%(self.instance.program,self.instance.instance,output))
		
	def _limit(self):
		resource.setrlimit(resource.RLIMIT_AS,(self.memout*1024,self.memout*1024))
		resource.setrlimit(resource.RLIMIT_RSS,(self.memout*1024,self.memout*1024))

	def run(self):
		count=0	
		lbwriter=LBWriter(self.outputfile)
		DEVNULL = open(os.devnull,'wb')
		for instance in self.instances:
			count+=1
			times=[]
			exitcodes=[]
			print "Instance %s/%s"%(count,len(self.instances))
			for portfolio in self.portfolios:
				print portfolio
				program=base.util.buildProgramString(self.dflat,instance,['--portfolio',portfolio])
				timestart=time.clock()
				myinput=open(instance.inputfile)
				call=subprocess.Popen(program,
						stdin=myinput,
						stdout=DEVNULL,
						stderr=DEVNULL,
						preexec_fn=self._limit)
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
				myinput.close()

			instance.runtimes=times
			instance.exitcodes=exitcodes
			lbwriter.write([instance])
			
			
		DEVNULL.close()
		return self.instances


	

