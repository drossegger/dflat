class TextWriter:
	def __init__(self,outputfile):
		self.outputfile=outputfile
	def write(self,text):
		f=open(self.outputfile,'a')
		f.write(text)
		f.close()
		return True

class LBWriter(TextWriter):
	def write(self,instances):
		f=open(self.outputfile,'a+')
		for instance in instances:
			f.write(instance.joinprogram+';'+instance.inputfile+';')
			myfeatures=[str(x) for x in instance.features]
			myruntimes=[str(x) for x in instance.runtimes]
			f.write(','.join(myfeatures)+';'+','.join(myruntimes)+'\n')
		f.close()
		return True


