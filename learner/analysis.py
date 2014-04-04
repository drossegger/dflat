from input.TextReader import LBReader
from output.TextWriter import CSVWriter
import numpy as np
a=LBReader('learningbase.csv')
x=a.read()
b=CSVWriter('lb.csv')
b.write(x)
norm=x[0][:-4]
norm=np.append(norm, "label")
x=np.delete(x,(0),axis=0)

for line in x:
	runtimes=line[line.shape[0]-4:]
	runtimes=[float(runtime) for runtime in runtimes]
	label=0
	for i in range(4):
		if runtimes[i] > 0:
			if label==0:
				label=i+1
			elif runtimes[i]<=runtimes[label-1]:
				label=i+1
	line=line[:-4]
	line=np.append(line,label)
	norm=np.vstack((norm,line))
c=CSVWriter("lbnorm.csv")
c.write(norm)


labels=[["term",0],["jumpy",0],["frumpy",0],["crafty",0],["none",0]]
norm=np.delete(norm,(0),axis=0)
for line in norm:
	label=int(line[line.shape[0]-1])
	if label == 0:
		labels[0][1]+=1
	elif label == 1:
		labels[1][1]+=1
	elif label == 2:
		labels[2][1]+=1
	elif label == 3:
		labels[3][1]+=1
	elif label == 4:
		labels[4][1]+=1
print labels


