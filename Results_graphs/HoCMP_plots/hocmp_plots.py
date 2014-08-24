#!/usr/bin/python

##Perundevi sametha Varadharaja Perumal

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import brewer2mpl
from matplotlib.lines import Line2D
import itertools
import random

###### Read data from file and store it in arrays #######
#data.split()
#print data
power_budget=[]
hocmp_value_2GHz=[]
hecmp_value_3GHz=[]
hecmp_value_vFreq=[]
hecmp_value_BT=[]

f = open (sys.argv[1], 'r')
data = f.readlines()
f.close()
for line in data:
  toks = line.strip().split(',')
  power_budget.append(toks[0])
  hocmp_value_2GHz.append(toks[1])
  hecmp_value_3GHz.append(toks[2])
  hecmp_value_vFreq.append(toks[3])
  hecmp_value_BT.append(toks[4])

fig, ax1 = plt.subplots()

###Create markers
markers = itertools.cycle(('d', '.', 'o', '*', '^', '+'))
##markers = itertools.cycle(('o', '*', '^'))

##Color Map
set2 = brewer2mpl.get_map('Set1', 'qualitative',9).mpl_colors

ax1.plot(power_budget, hocmp_value_2GHz, color=set2[0], label="2GHz_HoCMP", marker = markers.next(), markersize=4, linewidth=0.75)
ax1.plot(power_budget, hecmp_value_3GHz, color=set2[1], label="3GHz_HoCMP", marker = markers.next(), markersize=4, linewidth=0.75)
ax1.plot(power_budget, hecmp_value_vFreq, color=set2[3], label="vFreq_HoCMP", marker = markers.next(), markersize=4, linewidth=0.75)
ax1.plot(power_budget, hecmp_value_BT, color=set2[4], label="BoostThrottle_HoCMP", marker = markers.next(), markersize=4, linewidth=0.75)
ax1.set_ylabel('BIPS^2/W')
##ax1.set_ylabel('Speedup')
ax1.set_xlabel('Power Budget(W)')

plt.tight_layout()
plt.legend(loc=4)
output=str(sys.argv[2]) + ".png"
plt.savefig(output)
