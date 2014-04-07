import subprocess, re, base.util,sys,time


class FeatureExtractor:
	def __init__(self, instances):
		self.instances=instances

	def extract(self):
		for instance in self.instances:
			instance.features=instance.features+self.extractInstance(instance)
		return self.instances
	def extractFeatures(self,instance):
		return self

class ConfigFeatureExtractor(FeatureExtractor):
	def extractInstance(self,instance):
		features=[]
		if instance.defjoin:
			features.append((1,'defjoin'))
		else:
			features.append((0,'defjoin'))
		features.append((instance.normalization,'normalization'))
		features.append((instance.heuristic,'heuristic'))
		return features

class DynamicFeatureExtractor(FeatureExtractor):
	def __init__(self, dflat,instances):
		self.instances=instances
		self.dflat=dflat
		

	def extractInstance(self,instance):
		timestart=time.time()
		output = subprocess.Popen(base.util.buildProgramString(self.dflat,instance,['--ext-feat']),stdin=open(instance.inputfile),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		checker=True
		while True:
			if output.poll() is not None:
				break
			if time.time() - timestart >= 60:
				output.kill()
				time.sleep(5)
				checker=False
		result = re.compile(r'(.*\n)*begin features\n((.*\n)+)end features\n(.*\n)*',re.MULTILINE)
		lines = result.search(output.stdout.read()).group(2).splitlines()
		lines = [x.split(';') for x in lines]
		if checker==False:
			return [(x[0],-1) for x in lines]
		else:
			return [(x[0],float(x[1])) for x in lines]

class GringoFeatureExtractor(FeatureExtractor):
	def __init__(self, gringo,instances):
		self.instances=instances
		self.gringo=gringo
		#Gringo features, always add the feature in matching group 1
		self.features=[
				(re.compile('.*components\D*(\d+).*'),'gcomponents'),
				(re.compile('.*non-trivial\D*(\d+).*'),'gnontrivial'),
				(re.compile('.*predicates\D*(\d+).*'),'gpredicates'),
				(re.compile('.*rules\D*(\d+).*'),'grules'),
				(re.compile('.*constraints\D*(\d+).*'),'gconstraints')
				]

	def extractInstance(self, instance):
		call=subprocess.Popen('%s --gstats %s '%(self.gringo,instance.program),
				shell=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT)
		out=call.communicate()[0]
		rc=call.returncode
		if(rc!=0):
			sys.stderr.write("Error: gringo ended with errorcode %d"%rc)
			sys.exit(1)
		features=[]
		for f in self.features:
			feature=(float(f[0].search(out).group(1)),f[1])
			features.append(feature)
		return features

class EdgeFeatureExtractor(FeatureExtractor):
	def extractInstance(self,instance):
		f=open(instance.inputfile,'r')
		data=f.read()
		count=0
		for edge in instance.edges:
			for line in data.splitlines():
				if line.startswith(edge):
					count+=1
		return [(count,'nbredgefacts'),(len(instance.edges),'nbredgepred')]
