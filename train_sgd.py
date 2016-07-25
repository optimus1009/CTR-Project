#! /usr/bin/python

import random
import math

alpha = 0.03
iter = 20
l2 = 0.00
error = 0.05

file = open("train_feature", "r")
max_index = 0
for f in file:
	seg = f.strip().split("\t")
	for st in seg[1:]:
		index = int(st.split(":")[0])
		if index > max_index:
			max_index = index
file.close()

weight = range(max_index + 1)
delta = range(max_index + 1)
for i in range(max_index + 1):
	delta[i] = 0
	weight[i] = random.uniform(-0.01, 0.01)

for i in range(iter):
	
	file = open("train_feature", "r")
	loss = 0
	for f in file:
		seg = f.strip().split("\t")
		label = int(seg[0])
		s = 0.0
		for st in seg[1:]:
			index = int(st.split(":")[0])
			val = int(st.split(":")[1])
			s += weight[index]*val
		p = 1.0 / (1 + math.exp(-s))
#		print p
		g = p - label
#		loss = loss + (-label*math.log(p)-(1-label)*math.log(1 - p))
		for st in seg[1:]:
			index = int(st.split(":")[0])
			val = int(st.split(":")[1])
			delta[index] += g * g
			weight[index] -= alpha * (g*val + l2 * weight[index])#/(delta[index] + error)
#	print loss	
	file.close()

file = open("validate_feature", "r")
toWrite = open("pctr", "w+")
for f in file:
	seg = f.strip().split("\t")
	label = seg[0]
	s = 0.0
	for st in seg[1:]:
		index = int(st.split(":")[0])
                if(index > max_index) :
                    continue
		val = int(st.split(":")[1])
		s += weight[index]*val
	p = 1.0 / (1 + math.exp(-s))
	s = label + "," + str(p) + "\n"
	toWrite.write(s)

file.close()
toWrite.close()

file = open("test_data_feature", "r")
toWrite = open("pctrtest", "w+")
for f in file:
        seg = f.strip().split("\t")
        label = seg[0]
        s = 0.0
        for st in seg[1:]:
                index = int(st.split(":")[0])
                if(index > max_index) :
                    continue
                val = int(st.split(":")[1])
                s += weight[index]*val
        p = 1.0 / (1 + math.exp(-s))
        s = str(p) + "\n"
        toWrite.write(s)

file.close()
toWrite.close()
