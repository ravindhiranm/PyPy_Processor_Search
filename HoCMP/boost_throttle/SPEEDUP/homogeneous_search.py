#!/usr/bin/env pypy

##Shri Lakshmi Devi sametha Prahladhavaradhan
##Perundevi Sametha Devadhirajan
## An attempt to evaluate a multi-programmed case in determine core value

import os
import math
import sys
import random
import itertools
from collections import defaultdict

##benchmark_list = ['400.perlbench','401.bzip2','403.gcc','410.bwaves','416.gamess','429.mcf','433.milc','435.gromacs','444.namd','445.gobmk','450.soplex','453.povray','456.hmmer', '458.sjeng','459.GemsFDTD','462.libquantum','464.h264ref','470.lbm','471.omnetpp','473.astar','482.sphinx3','DUMMY']
##benchmark_list = ['400.perlbench','401.bzip2','403.gcc','429.mcf','445.gobmk','454.calculix','456.hmmer','458.sjeng','462.libquantum','464.h264ref','465.tonto','483.xalancbmk']

def toint(v):
	try:
		r = int(v)
		return r
	except ValueError, v:
		print(v)
		exit(1)

class statistics():
	def __init__(self):
		self.all_considered=0
		self.total_iterations=0

	def update_searched (self):
		self.all_considered += 1 

	def update_evaluated (self):
		self.total_iterations += 1

	def return_searched (self):
		return self.all_considered

	def return_evaluated (self):
		return self.total_iterations

class core_config():
	def __init__(self):
		self.app_perf=defaultdict(list)
		self.app_peak_power=defaultdict(list)
		self.app_runtime_power=defaultdict(list)
		self.app_cycles=defaultdict(list)
		self.app_instructions=defaultdict(list)
		self.app_speedup=defaultdict(list)
		
		self.core_attributes=[]
		self.core_area=None
		self.core_frequency=[]
		self.core_leak_power=[]
		self.core_peak_power=None
		self.coreId=None

		# example
		#self.app_perf["example"] = 1.0

	#### IPC
	def set_perf (self, app, perf):
		self.app_perf[app] = perf

	def get_perf (self, app):
		return self.app_perf[app]

	## Peak Power of Application
	def set_app_peak_power (self, app, p_power):
		self.app_peak_power[app] = p_power

	def get_app_peak_power (self, app):
		return self.app_peak_power[app]

	## Runtime Power of Application
	def set_runtime_power (self, app, power):
		self.app_runtime_power[app] = power 

	def get_runtime_power (self, app):
		return self.app_runtime_power[app]
	
	## Number of cycles
	def set_cycles (self, app, cycles):
		self.app_cycles[app] = cycles 

	def get_cycles (self, app):
		return self.app_cycles[app]

	## Number of Instructions
	def set_icount (self, app, count):
		self.app_instructions[app] = count

	def get_icount (self, app):
		return self.app_instructions[app]

	## Precompute Speedup for reducing evaluate time
	def set_speedup (self, app, speedUp):
		self.app_speedup[app] = speedUp

	def get_speedup (self, app):
		return self.app_speedup[app]


	### Core Attributes - App independant ####

	## Core ID 
	def set_coreID (self, core_id):
		self.coreId = core_id
 
	def get_coreID (self):
		return self.coreId 

	## Config details
	def set_attribute (self, core_att):
		self.core_attributes = core_att
 
	def get_attribute (self):
		return self.core_attributes 

	## Core Frequency
	def set_frequency (self, freq):
		self.core_frequency = freq

	def get_frequency (self):
		return self.core_frequency

	## Core Area
	def set_area (self, area):
		self.core_area = area

	def get_area (self):
		return self.core_area

	## Leakage Power
	def set_leak_power (self, leak_power):
		self.core_leak_power = leak_power 

	def get_leak_power (self):
		return self.core_leak_power

	## Maximum Power observed across app space
	def set_core_peak_power (self, peakPower):
		self.core_peak_power = peakPower

	def get_core_peak_power (self):
		return self.core_peak_power

def execution_time (total_cycles, frequency):
	time_period = 1.0/(float(frequency*10**9))
	ex_time = float(time_period) * float(total_cycles)
	return ex_time

def comb(n1,n2):
	n3=math.factorial(n1)/(math.factorial(n2)*math.factorial(n1-n2))
	return n3

def choose_random_config (total_cores, area_constraint, power_constraint):
        ##Assign bogus high values
        processor_area = 2*area_constraint
        processor_tdp = 2*power_constraint
        while (processor_area > area_constraint):

                processor_area = 0.0
                core=[]
                for i in range (0, total_cores):
                        core.append(all_configs[random.randint(0,224)])
                        ##print core
                        processor_area += float(core[i].get_area())
        return core
	
### How do you implement variable V an F in evaluate?
### idea 1: a.	create an pseudo processor comprising of (total_cores*total_frequency knobs)
###	    b.	schedule real workloads on 'n' cores and dummy workload on other cores
###		---- problem with this approach is that it will not scale and evaluate function will become time consuming

### idea 2: a.	Split the evaluate function
###	    b.	for each proc_config and multi-programmed workload, precompute the frequency combinations 
###		that will not exceed the power budget - put this into a list
###	    c.	evaluate all these and take the best
def evaluate(total_cores, core, area_constraint, power_constraint):
	frequency_combinations = [0,1,2]
	speedup_permutation_total_value=0 ##total core level speedup value of the schedule
	speedup_schedules=[]
	max_speedup_combination=[]

	for p in itertools.combinations(benchmark_list,total_cores):
		speedup_schedules=[]
		for r in itertools.permutations(p,total_cores):
			###use itertools.product to create variable frequency evaluations
			### so now each core will get a variable frequency assignment
			### that must be passed to get bips^2/w value at the frequency
			### need to extend class to obtain performance/power based on frequency - pretty simple
			###everything else will remain same
			freq_setting=itertools.product(frequency_combinations,frequency_combinations,frequency_combinations,frequency_combinations)
			for f in freq_setting:
				#print f
				speedup_permutation_total_value=0.0
				proc_power=0.0
			
				wl1=benchmark_list[benchmark_list.index(r[0])]
				wl2=benchmark_list[benchmark_list.index(r[1])]
				wl3=benchmark_list[benchmark_list.index(r[2])]
				wl4=benchmark_list[benchmark_list.index(r[3])]
				## Compute Peak Power dissipated by current Workload
				##proc_power = core[0].get_app_peak_power(benchmark_list[benchmark_list.index(r[0])])[f[0]] + core[1].get_app_peak_power(benchmark_list[benchmark_list.index(r[1])])[f[1]] + core[2].get_app_peak_power(benchmark_list[benchmark_list.index(r[2])])[f[2]] + core[3].get_app_peak_power(benchmark_list[benchmark_list.index(r[3])])[f[3]]
				proc_power = core[0].get_app_peak_power(wl1)[f[0]] + core[1].get_app_peak_power(wl2)[f[1]] + core[2].get_app_peak_power(wl3)[f[2]] + core[3].get_app_peak_power(wl4)[f[3]]
				if (proc_power > power_constraint):### Drop schedule if greater than power budget
					speedup_schedules.append(0)
				else:
					speedup_permutation_total_value = core[0].get_speedup(wl1)[f[0]] + core[1].get_speedup(wl2)[f[1]] + core[2].get_speedup(wl3)[f[2]] + core[3].get_speedup(wl4)[f[3]]
					speedup_schedules.append(speedup_permutation_total_value)
		max_speedup_combination.append(max(speedup_schedules))

	avg_core_speedup = sum(max_speedup_combination)/len(max_speedup_combination)
	return avg_core_speedup

def exhaustive_search(total_cores,area_constraint, power_constraint):
	#Initial core choices
	core_i = []
	core_i.append(all_configs[0])
	core_i = core_i*total_cores 
	avg_core_bips_i = 0.0 
	##avg_core_bips_i = evaluate (int(total_cores), core_i, float(area_constraint), float(power_constraint))
	##print total_cores,total_cores,core_i,area_constraint,power_constraint,avg_core_bips_i

	##Final Solution
	core_best = core_i
        avg_core_bips_best = avg_core_bips_i

	processor_area = 2*float(area_constraint) 
	processor_tdp = 2*float(power_constraint)
		
	for i in range(1,225):
		core_t=[]
		core_t.append(all_configs[i])
		core_t=core_t*int(total_cores)
		processor_area = float(core_t[0].get_area()) * float(total_cores)
		
		if (processor_area > float(area_constraint)):
			continue
		else:
			##print core_t
			avg_core_bips_t = evaluate(int(total_cores), core_t, float(area_constraint), float(power_constraint))
			if (avg_core_bips_t>avg_core_bips_i):
				core_i = core_t 
				avg_core_bips_i = avg_core_bips_t

			if (avg_core_bips_t>avg_core_bips_best):
				core_best = core_t
				avg_core_bips_best = avg_core_bips_t

	return core_best

############ Program Starts ########

### Intializing class instances for all cores in the library ###
all_configs = [core_config() for i in range (0,225)]

#### Creating a dictionary to map benchmark names to numbers ####
#### an attempt to speed up search ###
benchmark_map={}
bench_map=0
for line in file (sys.argv[1]):
	core_configt,benchmark,frequency1,frequency2,frequency3,ss_width,rob_size,iq_size,lq_size,sq_size,l1_icache_size,l1_dcache_size,l2_cache_size,instructions,cycles_freq1,cycles_freq2,cycles_freq3,ipc_freq1,ipc_freq2,ipc_freq3,area,peak_power_f1,peak_power_f2,peak_power_f3,runtime_dynamic_f1,runtime_dynamic_f2,runtime_dynamic_f3,total_leakage_f1,total_leakage_f2,total_leakage_f3=line.strip().split(',')
	
	## Get index for core instance
	something = core_configt.split('core_config')[1]
	r = toint(something)

	## mapping each benchmark to a number to speed up search
	if (benchmark_map == {}):
		benchmark_map[bench_map] = benchmark
	elif not benchmark in benchmark_map.values():
		bench_map += 1
		benchmark_map[bench_map] = benchmark

	#attributes=[int(ss_width),int(rob_size),int(iq_size),int(lq_size),int(sq_size),int(l1_icache_size),int(l2_cache_size)]
	attributes=[ss_width,rob_size,iq_size,lq_size,sq_size,l1_icache_size,l1_dcache_size,l2_cache_size]
	all_configs[r].set_icount(bench_map,int(instructions))
	all_configs[r].set_cycles(bench_map,[int(cycles_freq1),int(cycles_freq2),int(cycles_freq3)])
	all_configs[r].set_perf(bench_map,[float(ipc_freq1),float(ipc_freq2),float(ipc_freq3)])
	all_configs[r].set_runtime_power(bench_map,[float(runtime_dynamic_f1),float(runtime_dynamic_f2),float(runtime_dynamic_f3)])
	all_configs[r].set_app_peak_power(bench_map,[float(peak_power_f1),float(peak_power_f2),float(peak_power_f3)])
	all_configs[r].set_leak_power([float(total_leakage_f1),float(total_leakage_f2),float(total_leakage_f3)])
	all_configs[r].set_area(float(area))
	all_configs[r].set_frequency([float(frequency1),float(frequency2),float(frequency3)])
	all_configs[r].set_attribute(attributes)
	all_configs[r].set_coreID(r)
	##print "Hare Rama Hare Rama Hare Krishna Hare Hare"

#### to support legacy code - benchmark_list is used every where - see top of the program
##print benchmark_map
benchmark_list = range(0,len(benchmark_map))
##benchmark_list = ['400.perlbench','401.bzip2','403.gcc','429.mcf','445.gobmk','454.calculix','456.hmmer','458.sjeng','462.libquantum','464.h264ref','465.tonto','483.xalancbmk']
###print benchmark_list

##Hack to populate the first instance of the class - the input file has values from 
## core_config'1' => all_config[0] is never populated
all_configs[0] = all_configs [1]

### Setting the core peak power to the max observed peak power among applications
# for i in range (0,225):
# 	peakPower=[]
# 	for index in range(0, len(benchmark_list)):
# 		current_benchmark = benchmark_list[index]
# 		peakPower.append(all_configs[i].get_app_peak_power(current_benchmark))
# 	all_configs[i].set_core_peak_power(max(peakPower))
#for i in range (0,225):
	#print i,all_configs[i].get_core_peak_power()

### Setting Speedup observed copared to basic core
for index in range(0, len(benchmark_list)):
	for i in range (0,225):
		current_benchmark = benchmark_list[index]
		## Config1 is the simplest core in the study
		speedup=[]
		for freq in range(0,3):
			##print all_configs[1].get_cycles(current_benchmark)[0], all_configs[1].get_frequency()[0] 
			speedup.append(execution_time(all_configs[1].get_cycles(current_benchmark)[0],all_configs[1].get_frequency()[0])/execution_time(all_configs[i].get_cycles(current_benchmark)[freq],all_configs[i].get_frequency()[freq]))
		all_configs[i].set_speedup(current_benchmark,speedup)
		#print all_configs[i].get_speedup(current_benchmark)


## Assigning command-line  variables for human readability
total_cores=int(sys.argv[2])
area_constraint=float(sys.argv[3])
power_constraint=float(sys.argv[4])

#### Starting the search
optimized_cores = []
optimized_cores=exhaustive_search(total_cores,area_constraint,power_constraint)

## evaluation of the best core obtained from search
bestcore_goodness = evaluate (total_cores,optimized_cores,area_constraint,power_constraint)

## Writing output to file
fileName = 'HoCMP_' + sys.argv[2] + 'C_' + sys.argv[3] + 'mm_' + sys.argv[4] + 'W'
myFile = open (fileName, 'w')
myFile.write("################ SRI ###############\n")
myFile.write("\n")
myFile.write("Average Speedup: " + str(bestcore_goodness))
myFile.write("\n"+"\n")

for i in range (0, len(optimized_cores)):
        config_detail = optimized_cores[i].get_attribute()
        myFile.write( "Core_" + str(optimized_cores[i].get_coreID()) + ";Area:"  + str(optimized_cores[i].get_area()) + ";Peak_Power:" + str(optimized_cores[i].get_core_peak_power()) + ";h264ref_Power:" + str(optimized_cores[i].get_runtime_power(9)) + "\n")
    	myFile.write("F=" + str(optimized_cores[i].get_frequency()) + "-W=" + config_detail[0] + "-ROB=" + config_detail[1] + "-IQ=" + config_detail[2] + "-LQ=" + config_detail[3] + "-SQ=" + config_detail[4] + "-L1_I$=" + config_detail[5] + "-L1_D$=" + config_detail[6] + "-L2=" + config_detail[7] + "\n" + "\n")
myFile.close()

fileN = fileName + '.json' 
myFile = open (fileN, 'w')
myFile.write("series: [{" + "\n")
myFile.write("  name: 'Largest_Core'," + "\n")
myFile.write("  data: [3,4,5,2,2,4],\n")
myFile.write("  pointPlacement: 'on'\n")
myFile.write("}\n")

for i in range (0, len(optimized_cores)):
	config_detail = optimized_cores[i].get_attribute()

	####attributes=[ss_width,rob_size,iq_size,lq_size,sq_size,l1_icache_size,l1_dcache_size,l2_cache_size]
	##Check ROB Size to Determine Inorder of OoO	
	if (int(config_detail[1])==4):
		config_detail1 = 1
	elif (int(config_detail[1])==40):
	        config_detail1=2
	elif (int(config_detail[1])==128):
	        config_detail1=3
	elif (int(config_detail[1])==168):
	        config_detail1=4
	elif (int(config_detail[1])==192):
	        config_detail1=5
	else:
	        config_detail1=10000
	
	##L1 I$
	if (int(config_detail[5])==16):
	        config_detail2=1
	elif (int(config_detail[5])==32):
	        config_detail2=2
	else:
	        config_detail5=10000
	
	##L1 D$
	if (int(config_detail[6])==32):
	        (config_detail3)=1
	elif (int(config_detail[6])==64):
	        (config_detail3)=2
	else:
	        config_detail5=10000
	
	##L2
	if (int(config_detail[7])==128):
	        config_detail4=1
	elif (int(config_detail[7])==256):
	        config_detail4=2
	elif (int(config_detail[7])==512):
	        config_detail4=3
	elif (int(config_detail[7])==1024):
	        config_detail4=4
	else:
	        config_detail4=10000
    
	myFile.write(" ,{name: 'core_" + str(optimized_cores[i].get_coreID()) + "'," + "\n")
	myFile.write("  data: [" + str(optimized_cores[i].get_frequency()) + "," + str(config_detail[0]) + "," + str(config_detail1) + "," + str(config_detail2) + "," + str(config_detail3) + "," + str(config_detail4) + "]," +"\n")
	myFile.write("  pointPlacement: 'on'\n")
	myFile.write("}\n")
myFile.write("]\n")
myFile.close()

fileName += ".csv"
myFile = open (fileName, 'w')

for index in range(len(benchmark_list)):
	##myFile.write(str(benchmark_list[index]) + ", config core" + str(optimized_cores[i]) + ", " + str(all_configs[optimized_cores[i]].get_perf(benchmark_list[index])) + ", " + str(all_configs[optimized_cores[i]].get_power(benchmark_list[index])) + ", " + str( all_configs[optimized_cores[i]].get_extime(benchmark_list[index])) + ", " + str(Energy) + ", " + str(bips_per_watt2(all_configs[optimized_cores[i]].get_perf(benchmark_list[index]),2, all_configs[optimized_cores[i]].get_power(benchmark_list[index]))))
	myFile.write(str(benchmark_map[index]) + ", config core" + str(optimized_cores[0].get_coreID()) + ", " + str(optimized_cores[0].get_perf(benchmark_list[index])) + ", " + str(optimized_cores[0].get_runtime_power(benchmark_list[index])) + ", " + str(optimized_cores[0].get_speedup(benchmark_list[index])))
	myFile.write("\n")
myFile.close()
