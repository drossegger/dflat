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
			print instance.runtimes
			f.write(instance.program+';'+instance.inputfile+';')
			myfeatures=[str(x) for x in instance.features]
			myexitcodes=[str(x) for x in instance.exitcodes]
			myruntimes=[str(x) for x in instance.runtimes]
			f.write(','.join(myfeatures)+';'+','.join(myruntimes)+';'+','.join(myexitcodes)+'\n')
		f.close()
		return True


class CSVWriter(TextWriter):
	def write(self,array,delim=';'):
		f=open(self.outputfile,'a+')
		for line in array:
			f.write(';'.join(line)+'\n');
		f.close()
		return True
