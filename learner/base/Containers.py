class Instance:
	program=''
	multilevel=False
	exchange=''
	inputfile=''
	edges=[]
	seed=1
	defjoin=False
	normalization='none'
	problemtype='counting'
	features=[]
	runtimes=[]
	exitcodes=[]
	heuristic='min-degree'
	def __init__(self):
		self.features=[]
		self.runtimes=[]
		self.exitcodes=[]
		self.edges=[]

class Feature:
	name=''
	nominal=False	
	column=0
	def __init__(self,name,nominal):
		self.name=name
		self.nominal=nominal

	
