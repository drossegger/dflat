from test.FeatureExtractors import *
from input.ConfigParser import ConfigParser 
from input.TextReader import LBReader
from base.Containers import Instance
from classification.Classifier import SVMClassifier
import argparse as ap

c=ConfigParser()
def learn(args):
	featureExtractors=[GringoFeatureExtractor(c.gringo,c.instances),EdgeFeatureExtractor(c.instances),ConfigFeatureExtractor(c.instances),DynamicFeatureExtractor(c.dflat,c.instances)]
	for f in featureExtractors:
		instances=f.extract()
	r=RunTest(c.dflat,instances,c.portfolios,outputfile=args.learningbase)
	instances=r.run()
	#TODO Test

def generateModel(args):
	lb=LBReader(args.learningbase,c.features).read()
	clf=SVMClassifier(c,lb[0],lb[1])
	clf.prepare()
	clf.buildModel()
	clf.saveModel(args.model)

def solve(args):
	i=Instance()
	i.program=args.encoding
	i.inputfile=args.instance
	i.edges.append(args.e)
	fe=[GringoFeatureExtractor(c.gringo,[i]),EdgeFeatureExtractor([i]),DynamicFeatureExtractor(c.dflat,[i])]
	for f in fe:
		i=f.extract()
	clf=SVMClassifier()
	clf=clf.loadModel(args.model)
	print clf.predict(i[0].features)


cliparse=ap.ArgumentParser(description='D-FLAT Learner, make sure to edit config.xml to your needs.')
clisp=cliparse.add_subparsers()

parser_learn=clisp.add_parser('learn')
parser_learn.add_argument('--learningbase',default='learningbase.csv',help="set the learningbase file")
parser_learn.set_defaults(func=learn)

parser_gmod=clisp.add_parser('genmod')
parser_gmod.add_argument('--learningbase',default='learningbase.csv',help="set the learningbase file")
parser_gmod.add_argument('--model',default='default.mod',help="set the model file")
parser_gmod.set_defaults(func=generateModel)

parser_solve=clisp.add_parser('solve')
parser_solve.add_argument('--model',default='default.mod',help="set the model file")
parser_solve.add_argument('-e',help="specify (multiple) edge predicates")
parser_solve.add_argument('--args',default="")
parser_solve.add_argument('encoding')
parser_solve.add_argument('instance')
parser_solve.set_defaults(func=solve)

args=cliparse.parse_args()

args.func(args)
