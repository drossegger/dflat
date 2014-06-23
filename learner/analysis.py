from input.TextReader import LBReader
from output.TextWriter import CSVWriter
import numpy as np
import sys

a=LBReader(sys.argv[1])
x=a.read()
b=CSVWriter(sys.argv[2])
b.write(x)
norm=x[0][:-5]
norm=np.append(norm, "label")
x=np.delete(x,(0),axis=0)

for line in x:
	runtimes=line[line.shape[0]-5:]
	runtimes=[float(runtime) for runtime in runtimes]
	label=1
	if len(set(runtimes)) == 1:
		if runtimes[0]<0:
			label=0
		else:
			label=6
	else:
		for i in range(5):
			if runtimes[i]<=runtimes[label-1]:
				label=i+1
		
	line=line[:-5]
	line=np.append(line,label)
	norm=np.vstack((norm,line))
c=CSVWriter(sys.argv[3])
c.write(norm)


labels=[["term",0],["jumpy",0],["frumpy",0],["crafty",0],["none",0],["nopre",0]]
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
	elif label == 5:
		labels[5][1]+=1
print labels


