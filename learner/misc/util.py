from Containers import Instance
from ConfigParser import ConfigParser

def buildProgramString(dflat,instance,arguments=''):
	ps=dflat +arguments+ ' --seed ' + str(instance.seed) + ' --tables'
	for edge in instance.edges:
		ps=ps+' -e ' + edge
	if instance.multilevel:
		ps=ps+' --multi-level'
	ps=ps+' -p ' + instance.program
	ps=ps + ' < ' + instance.inputfile
	return ps
	
