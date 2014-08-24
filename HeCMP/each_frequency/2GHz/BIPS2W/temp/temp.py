#!/usr/bin/env pypy

import itertools

benchmark_list = range(0,12)
processor_size = range(0,4)
total_cores = 2

###Create multiprogrammed workload combinations to be used while evaluating goodness
workloads = list(itertools.combinations(benchmark_list,total_cores))
for i in workloads:
    for j in i:
        print j,
    print "\n",

### Create indices for permutations of workloads
#processor_size = range(0,total_cores)
#permute = list(itertools.permutations(processor_size,total_cores))
#for i in permute:
#    for j in i:
#        print j,
#    print "\n",
#
#print permute

