from Containers import Instance
from ConfigParser import ConfigParser

def buildProgramString(dflat,instance,arguments=''):
	ps=dflat +arguments+ ' --seed ' + str(instance.seed) + ' --tables' + ' -n ' + str(instance.normalization) + ' --elimination '+str(instance.heuristic)
	for edge in instance.edges:
		ps=ps+' -e ' + edge
	if instance.multilevel:
		ps=ps+' --multi-level'
	if instance.defjoin:
		ps=ps+' --default-join'
	ps=ps+' -p ' + instance.program
	ps=ps + ' < ' + instance.inputfile
	return ps
	
