from test.FeatureExtractors import GringoFeatureExtractor
from test.FeatureExtractors import EdgeFeatureExtractor
from test.FeatureExtractors import ConfigFeatureExtractor
from test.FeatureExtractors import DynamicFeatureExtractor
from test.RunTest import RunTest 
from input.ConfigParser import ConfigParser
def myFilter(i):
	for f in i.features:
		if f[1]==-1:
			return False
	return True

c=ConfigParser()
gfe=GringoFeatureExtractor(c.gringo, c.instances)
efe=EdgeFeatureExtractor(c.instances)
cfe=ConfigFeatureExtractor(c.instances)
dfe=DynamicFeatureExtractor(c.dflat,c.instances)
instances=gfe.extract()
instances=efe.extract()
instances=cfe.extract()
instances=dfe.extract()
instances=[i for i in instances if myFilter(i)]
r=RunTest(c.dflat,instances,c.portfolios)
instances=r.run()


