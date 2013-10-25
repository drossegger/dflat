import sys
from test.FeatureExtractor import FeatureExtractor
from test.RunTest import RunTest 
from output.TextWriter import *
from misc.ConfigParser import *

c=ConfigParser()
f=FeatureExtractor(c.dflat, c.instances)
instances=f.extract()
r=RunTest(c.dflat,instances,c.portfolios)
instances=r.run()
lbw=LBWriter('learningbase.csv')
if lbw.write(instances)==False: 
	print "ERROR writing File"
	sys.exit(1)

for instance in instances:
	print instance.features
	print instance.runtimes
