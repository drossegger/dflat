#!/usr/bin/python
from timeit import Timer
import xml.etree.ElementTree as ET
import subprocess,re,os,sys

def buildProgramString(instance):
	arg=['-s','1','-p','counting']
	for edge in instance.iter('edge'):
		arg.append('-e')
		arg.append(edge.text)
	mlvl=instance.find('multi-level')
	if mlvl != None:
		arg.append('--multi-level')
	exch=instance.find('exchange-program')
	if exch != None:
		arg.append('-x')
		arg.append(exch.text)
	arg.append(instance.find('join-program').text)
	arg.append('<')
	arg.append(instance.find('input-file').text)
	return arg

def extractFeatures(arg,features):
	arg.insert(1,'--only-extract')
	output=subprocess.check_output(' '.join(arg),shell=True)
	arg.pop(1)
	p=re.compile(r'(.*\n)*begin features\n((.*\n)+)end features\n(.*\n)*',re.MULTILINE)
	lines=p.match(output).group(2).splitlines()
	lines=[x.split(';') for x in lines]
	for line in lines:
		feature=features.find('./feature[@name="'+line[0]+'"]')
		if feature==None:
			line.append(line[1])
		else:
			line[1]=float(line[1])
			size=float(feature.get('size',1))
			limitLo=int(line[1]/size)*size
			limitHi=round(line[1]/size)*size
			maxval=float(feature.get('max',1000000))
			minval=float(feature.get('min',0))
			if line[1]<minval:
				line[1]=0
				line.append(minval)
			elif line[1]>maxval:
				line[1]=maxval
				line.append(0)
			else:
				line[1]=limitLo
				line.append(limitHi)
	return lines

def writeCSV(portfolios,features,performance):
		for feature in features:
			featurename=feature.pop(0)
			if(os.path.exists(featurename+'.csv')):
				f=open(featurename+'.csv','a+')
				#csvString=f.read()
				#p=re.compile(str(feature[0])+'\;'+str(feature[1])+'.*')#TODO Escape dots?
				#if p.search(csvString)!=None:
				#	f.close()
					#TODO Does nothing atm
				#else:
				#	f.write('\n')
				f.write(';'.join([str(x) for x in feature+performance])+'\n')
				f.close()
			else:
				f=open(featurename+'.csv','w')
				f.write(';'.join(portfolios)+'\n')
				f.write(';'.join([str(x) for x in feature+performance])+'\n')
				f.close()

def finalize(features):
	for xmlfeature in features.iter('feature'):
		feature=xmlfeature.attrib.get('name')
		if(os.path.exists(feature+'.csv')):
			f=open(feature+'.csv','r')
			featurelines=f.read().splitlines();
			performance=[line.split(';') for line in featurelines]
			firstline=performance.pop(0)	
			performance=[[float(val) for val in line] for line in performance]
			indeces=set([val[0] for val in performance])

			finPerformance=[]
			for index in indeces:
				indexentry=[line for line in performance if line[0]==index]
				portfolioperformances=[]	
				for colindex in range(2,len(indexentry[0])):
					col=[row[colindex] for row in indexentry]
					portfolioperformances.append(sum(col)/len(col))
				myhelper=[indexentry[0][0],indexentry[0][1]]+portfolioperformances
				finPerformance.append(myhelper)
			f.close()
			f=open(feature+'.csv','w')
			f.write(';'.join(firstline)+'\n')
			for line in finPerformance:
				line=[str(val) for val in line]
				f.write(';'.join(line)+'\n')
			f.close()
		else:
			print 'Error, featurefile not found'
			quit()
def learn(root,numberseeds):
	portfolios=['','']+[portfolio.text for portfolio in root.iter('portfolio')]
	for instance in root.iter('instance'):
		arg=[root.find('dflat').text]+buildProgramString(instance)
		for seed in range(numberseeds):
			times=[]
			features=extractFeatures(arg,root.find('features'))
			print features
			for portfolio in root.iter('portfolio'):
				arg[2]=''+str(seed)
				arg.insert(1,portfolio.text)
				arg.insert(1,'--portfolio')
				print ' '.join(arg)
				t=Timer('subprocess.call("%s",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)' % ' '.join(arg),setup='import subprocess')
				arg.pop(1)
				arg.pop(1)
				times.append(min(t.repeat(repeat=2,number=1)))
			print features
			print min(times)
			print [x/min(times) for x in times]
			writeCSV(portfolios,features,[x/min(times) for x in times])



tree=ET.parse('config.xml')
if len(sys.argv)==2 :
	if(sys.argv[1]=='--finalize'):
		finalize(tree.getroot().find('features'))
	else:
		print 'Wrong command line arguments'
		quit()
elif len(sys.argv)==3 :
	if sys.argv[1]=="--seeds" :
		learn(tree.getroot(),int(sys.argv[2]))
	else:
		print 'Wrong command line arguments'
		quit()
elif len(sys.argv)>3:
	print 'Wrong command line arguments'
	quit()
else:
	learn(tree.getroot(),1)



