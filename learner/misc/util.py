from Containers import Instance
from ConfigParser import ConfigParser

def buildProgramString(dflat,instance,arguments=''):
	ps=dflat +arguments+ ' -s ' + str(instance.seed) + ' -p ' + instance.problemtype
	for edge in instance.edges:
		ps=ps+' -e ' + edge
	if instance.multilevel:
		ps=ps+' --multi-level'
	if instance.exchprogram!='':
		ps=ps+' -x ' + instance.exchprogram
	ps=ps + ' ' + instance.joinprogram+ ' < ' + instance.inputfile
	return ps
	
