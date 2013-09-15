#!/usr/bin/python
from timeit import Timer
import xml.etree.ElementTree as ET
import subprocess,re,os

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
	p=re.compile('begin features\n(.*)\nend features.*')
	lines=p.match(output).group(1).splitlines()
	lines=[x.split(';') for x in lines]
	for line in lines:
		feature=features.find('./feature[@name="'+line[0]+'"]')
		if feature==None:
			line.append(line[1])
		else:
			line[1]=float(line[1])
			size=feature.find('size')
			if size!=None:
				size=float(size.text)
				limitLo=int(line[1]/size)*size
				limitHi=round(line[1]/size)*size
				maxval=float(feature.find('max').text)
				minval=float(feature.find('min').text)
				if line[1]<minval:
					line[1]=0
					line.append(minval)
				elif line[1]>maxval:
					line[1]=maxval
					line.append(0)
				else:
					line[1]=limitLo
					line.append(limitHi)
			else:
				line.append(line[1])
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

tree=ET.parse('config.xml')
root=tree.getroot()
portfolios=['','']+[portfolio.text for portfolio in root.iter('portfolio')]
for instance in root.iter('instance'):
	arg=[root.find('dflat').text]+buildProgramString(instance)
	times=[]
	features=extractFeatures(arg,root.find('features'))
	for portfolio in root.iter('portfolio'):
		arg.insert(1,portfolio.text)
		arg.insert(1,'--portfolio')
		print ' '.join(arg)
		t=Timer('subprocess.call("%s",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)' % ' '.join(arg),setup='import subprocess')
		arg.pop(1)
		arg.pop(1)
		times.append(min(t.repeat(repeat=4,number=1)))
	print features
	print min(times)
	print [x/min(times) for x in times]
	writeCSV(portfolios,features,[x/min(times) for x in times])

