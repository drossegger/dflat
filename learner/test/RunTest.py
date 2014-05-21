from output.TextWriter import LBWriter
import time,subprocess
import base.util
import sys,resource,os,threading

class RunCmd(threading.Thread):
	def __init__(self,cmd,timeout,inp,memout):
		threading.Thread.__init__(self)
		self.cmd=cmd
		self.timeout=timeout
		self.inp=inp
		self.err=None
		self.memout=memout
		self.exitcode=None
	def _limit(self):
		resource.setrlimit(resource.RLIMIT_AS,(self.memout*1024,self.memout*1024))
		resource.setrlimit(resource.RLIMIT_RSS,(self.memout*1024,self.memout*1024))

	def run(self):
		self.call=subprocess.Popen(self.cmd,
						stdin=open(self.inp),
						stderr=subprocess.PIPE,
						preexec_fn=self._limit)
		self.exitcode=self.call.wait()
		self.err=self.call.stderr.read()
	def Run(self):
		self.start()
		self.join(self.timeout)
		if self.is_alive():
			self.call.kill()
			self.exitcode=self.call.poll()
			self.join()
	def getError(self):
		return self.err
	def getExit(self):
		return self.exitcode

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
				call=RunCmd(program,self.maxtime,instance.inputfile,self.memout)
				while True:
					if call.getExit() is not None:
						exitcodes.append((portfolio,call.returncode))
						if call.getExit()==-15:
							times.append((portfolio,-100))	
						else:
							times.append((portfolio, base.util.extractTime(call.getError())))
						break
					time.sleep(1)
							

			instance.runtimes=times
			instance.exitcodes=exitcodes
			lbwriter.write([instance])
			
			
		return self.instances


	

