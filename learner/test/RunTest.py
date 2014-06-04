from output.TextWriter import LBWriter
import time,subprocess
import base.util
import sys,resource,os,signal

class RunTest:
	memout=8388608	

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
				program=base.util.buildProgramString(self.dflat,instance,['--portfolio',portfolio])
				timestart=time.time()
				myinput=open(instance.inputfile)
				call=subprocess.Popen(program,
						stdin=myinput,
						stdout=DEVNULL,
						stderr=subprocess.PIPE,
						preexec_fn=self._limit,
						shell=False)
				pid=call.pid
				while True:
					if call.poll() is not None:
						break
					if time.time() - timestart > self.maxtime:
						call.kill()
						print "killed call after %d"%(time.time()-timestart)
						time.sleep(5)
						print "kill failed, forcing kill, pid: %d"%(pid)
						os.kill(pid+1,signal.SIGKILL)
						times.append((portfolio,"real",-100))	
						times.append((portfolio,"user",-100))	
						times.append((portfolio,"sys",-100))	

					time.sleep(1)

				timeend=time.time()
				exitcodes.append((portfolio,"rc",call.returncode))

				if timeend - timestart < self.maxtime:
					stderr=call.stderr.read()
					times.append((portfolio,"real", base.util.extractTime(stderr,"real")))
					times.append((portfolio,"sys", base.util.extractTime(stderr,"sys")))
					times.append((portfolio,"user", base.util.extractTime(stderr,"user")))
					print "%s finished after %s"%(portfolio,base.util.extractTime(stderr,"real"))
							

			instance.runtimes=times
			instance.exitcodes=exitcodes
			lbwriter.write([instance])
			
			
		return self.instances


	

