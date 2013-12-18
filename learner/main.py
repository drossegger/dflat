import sys
from test.FeatureExtractors import GringoFeatureExtractor
from test.RunTest import RunTest 
from output.TextWriter import *
from misc.ConfigParser import *
from misc.util import buildProgramString

c=ConfigParser()
f=GringoFeatureExtractor(c.gringo, c.instances)
instances=f.extract()
for instance in instances:
	 for feature in instance.features:
		 print feature
r=RunTest(c.dflat,instances,c.portfolios)
instances=r.run()
lbw=LBWriter('learningbase.csv')
if lbw.write(instances)==False: 
	print "ERROR writing File"
	sys.exit(1)

#print buildProgramString(c.dflat,instance,' --portfolio none')
for instance in instances:
	print instance.features
	print instance.runtimes
