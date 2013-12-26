import sys
from test.FeatureExtractors import GringoFeatureExtractor
from test.FeatureExtractors import EdgeFeatureExtractor
from test.FeatureExtractors import ConfigFeatureExtractor
from test.FeatureExtractors import DynamicFeatureExtractor
from test.RunTest import RunTest 
from output.TextWriter import *
from misc.ConfigParser import *
from misc.util import buildProgramString

c=ConfigParser()
gfe=GringoFeatureExtractor(c.gringo, c.instances)
efe=EdgeFeatureExtractor(c.instances)
cfe=ConfigFeatureExtractor(c.instances)
dfe=DynamicFeatureExtractor(c.dflat,c.instances)
instances=gfe.extract()
instances=efe.extract()
instances=cfe.extract()
instances=dfe.extract()
for instance in instances:
	 for feature in instance.features:
		 print feature
r=RunTest(c.dflat,instances,c.portfolios)
instances=r.run()
#lbw=LBWriter('learningbase.csv')
#if lbw.write(instances)==False: 
#	print "ERROR writing File"
#	sys.exit(1)

#print buildProgramString(c.dflat,instance,' --portfolio none')
#for instance in instances:
#	print instance.features
#	print instance.runtimes
