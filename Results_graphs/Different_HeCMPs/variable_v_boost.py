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
hocmp_value=[]
hecmp_value=[]
improvement=[]

f = open (sys.argv[1], 'r')
data = f.readlines()
f.close()
for line in data:
  toks = line.strip().split(',')
  power_budget.append(toks[0])
  hocmp_value.append(toks[1])
  hecmp_value.append(toks[2])
  improvement.append(((float(toks[2])/float(toks[1]))-1)*100)

fig, ax1 = plt.subplots()
num_plots=3

###Create markers
#markers = itertools.cycle(('+', '.', 'o', '*', '^'))
markers = itertools.cycle(('o', '*', '^'))

##Color Map
set2 = brewer2mpl.get_map('Set1', 'qualitative',9).mpl_colors

t=1
ax1.plot(power_budget, improvement, color=set2[t], label=sys.argv[2], marker = markers.next(), markersize=4, linewidth=2)
ax1.set_xlabel('Power Budget (W)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('Improvement(%)', color=set2[t])
for tl in ax1.get_yticklabels():
    tl.set_color(set2[t])

##t1=random.randint(0,7)
##while (t1 == t):
##	t1=random.randint(0,8)
t1=8
ax2 = ax1.twinx()
ax2.plot(power_budget, hocmp_value, color=set2[t1], label="HeCMP_v_freq", marker = markers.next(), markersize=4, linewidth=0.5)
ax2.plot(power_budget, hecmp_value, color=set2[t1], label="BoostThrottle_HeCMP", marker = markers.next(), markersize=4, linewidth=0.5)
#ax2.set_ylabel('BIPS^2/W', color=set2[t1])
ax2.set_ylabel('Speedup', color=set2[t1])
for tl in ax2.get_yticklabels():
    tl.set_color(set2[t1])

plt.tight_layout()
plt.legend(loc=2)
output=str(sys.argv[2]) + ".png"
plt.savefig(output)
