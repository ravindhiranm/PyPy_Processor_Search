#!/usr/bin/env pypy

##Shri Lakshmi Devi sametha Prahladhavaradhan
##Perundevi Sametha Devadhirajan
## An attempt to evaluate a multi-programmed case in determine core value

##import os
import math
import sys
import random
import itertools

##benchmark_list = ['400.perlbench','401.bzip2','403.gcc','410.bwaves','416.gamess','429.mcf','433.milc','435.gromacs','444.namd','445.gobmk','450.soplex','453.povray','456.hmmer', '458.sjeng','459.GemsFDTD','462.libquantum','464.h264ref','470.lbm','471.omnetpp','473.astar','482.sphinx3','DUMMY']
##benchmark_list = ['400.perlbench','401.bzip2','403.gcc','429.mcf','445.gobmk','454.calculix','456.hmmer','458.sjeng','462.libquantum','464.h264ref','465.tonto','483.xalancbmk']

def toint(v):
    try:
        r = int(v)
        return r
    except ValueError, v:
        print(v)
        exit(1)


class core_config():
    def __init__(self):
        self.app_perf={}
        self.app_peak_power={}
        self.app_runtime_power={}
        self.app_cycles={}
        self.app_instructions={}
        self.app_speedup={}#speedup obtained over base core

        self.core_attributes=[]
        self.core_area=None
        self.core_frequency=None
        self.core_leak_power=None
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

def bips_per_watt (ipc, frequency, power):
    #get total_instructions = frequency*ipc and divide it by 10^9
    ##but have to mul by 1*10**9 -if frequency represented in GHz
    bips = float(frequency)*float(ipc)
    bips_per_watt = float(bips)/float(power)
    return bips_per_watt

def bips_per_watt2 (ipc, frequency, power):
    bips2 = (float(frequency)*float(ipc))**2
    bips2_per_watt = float(bips2)/float(power)
    return bips2_per_watt

def bips_per_watt3 (ipc, frequency, power):
    bips3 = (float(frequency)*float(ipc))**3
    bips3_per_watt = float(bips3)/float(power)
    return bips3_per_watt

def execution_time (total_cycles, frequency):
    time_period = 1.0/(float(frequency*10**9))
    ex_time = float(time_period) * float(total_cycles)
    return ex_time

def comb(n1,n2):
    n3=math.factorial(n1)/(math.factorial(n2)*math.factorial(n1-n2))
    return n3

def evaluate(total_cores, core, area_constraint, power_constraint):
    speedup_permutation_total_value=0 ##total core level speedup value of the schedule
    max_speedup_combination=[]
    total_eval_range = range(0,total_cores)

    for p in itertools.combinations(benchmark_list,total_cores):
        speedup_permutation_total_value=0
        for i in total_eval_range:
            current_core=core[i]
            speedup_permutation_total_value+=all_configs[current_core].get_speedup(p[i])
        max_speedup_combination.append(speedup_permutation_total_value)

    avg_core_speedup = sum(max_speedup_combination)/len(max_speedup_combination)
    return avg_core_speedup

def exhaustive_search(total_cores, area_constraint, power_constraint):
    #Initial core choices
    core_i = []
    core_i.append(0)
    core_i = core_i*total_cores
    avg_core_bips_i = evaluate (int(total_cores), core_i, float(area_constraint), float(power_constraint))
    ##print total_cores,powered_cores,core_i,area_constraint,power_constraint,avg_core_bips_i

    # overall best solution
    core_best = core_i
    avg_core_bips_best = avg_core_bips_i

    processor_area = 2*float(area_constraint)
    processor_tdp = 2*float(power_constraint)

    for i in range(1,673):
        core_t=[]
        core_t.append(i)
        core_t=core_t*int(total_cores)
        processor_area = float(all_configs[core_t[0]].get_area()) * float(total_cores)
        processor_tdp = float(all_configs[core_t[0]].get_core_peak_power()) * float(total_cores)
        #print core_t

        if (processor_area > float(area_constraint) or processor_tdp > float(power_constraint)):
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

all_configs = [core_config() for i in range (0,673)]


#### Creating a dictionary to map benchmark names to numbers ####
#### an attempt to speed up search ###
benchmark_map={}
bench_map=0

for line in file (sys.argv[1]):
    core_configt,benchmark,frequency,ss_width,rob_size,iq_size,lq_size,sq_size,l1_icache_size,l1_dcache_size,l2_cache_size,instructions,cycles,ipc,ex_time,area,peak_power,runtime_dynamic,total_leakage=line.strip().split(',')

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
    all_configs[r].set_cycles(bench_map,int(cycles))
    all_configs[r].set_perf(bench_map,float(ipc))
    all_configs[r].set_runtime_power(bench_map,float(runtime_dynamic))
    all_configs[r].set_app_peak_power(bench_map,float(peak_power))
    all_configs[r].set_leak_power(float(total_leakage))
    all_configs[r].set_area(float(area))
    all_configs[r].set_frequency(float(frequency))
    all_configs[r].set_attribute(attributes)
    all_configs[r].set_coreID(r)

#### to support legacy code - benchmark_list is used every where - see top of the program
##print benchmark_map
benchmark_list = range(0,len(benchmark_map))
##benchmark_list = ['400.perlbench','401.bzip2','403.gcc','429.mcf','445.gobmk','454.calculix','456.hmmer','458.sjeng','462.libquantum','464.h264ref','465.tonto','483.xalancbmk']
###print benchmark_list

##Hack to populate the first instance of the class - the input file has values from
## core_config'1' => all_config[0] is never populated
all_configs[0] = all_configs [1]

### Setting the core peak power to the max observed peak power among applications
for i in range (0,673):
    peakPower=[]
    for index in range(0, len(benchmark_list)):
        current_benchmark = benchmark_list[index]
        peakPower.append(all_configs[i].get_app_peak_power(current_benchmark))
    all_configs[i].set_core_peak_power(max(peakPower))

### Setting Speedup observed copared to basic core
for index in range(0, len(benchmark_list)):
    for i in range (0,673):
        current_benchmark = benchmark_list[index]
        if (current_benchmark == 'DUMMY'):
            speedup=0
            all_configs[i].set_speedup(benchmark,speedup)
        else:
            ## Config865 is the simplest core in the study
            speedup=execution_time(all_configs[1].get_cycles(current_benchmark),all_configs[1].get_frequency())/execution_time(all_configs[i].get_cycles(current_benchmark),all_configs[i].get_frequency())
            all_configs[i].set_speedup(current_benchmark,speedup)
        ##	print all_configs[i], current_benchmark, all_configs[i].get_speedup(current_benchmark)



###### Assigning variables for human readability ####
total_cores=int(sys.argv[2])
area_constraint=float(sys.argv[3])
power_constraint=float(sys.argv[4])

#### Starting the search
optimized_cores = []
optimized_cores=exhaustive_search(total_cores, area_constraint, power_constraint)

## evaluation of the best core obtained from search
bestcore_speedup = evaluate (total_cores ,optimized_cores, area_constraint, power_constraint)

## Writing output to file
fileName = 'HoCMP_' + str(total_cores) + 'C_' + str(int(area_constraint)) + 'mm_' + str(int(power_constraint)) + 'W'
myFile = open (fileName, 'w')
myFile.write("Chosen Cores\n" + str(optimized_cores))
myFile.write("\n")
myFile.write("Average Speedup: " + str(bestcore_speedup))
myFile.write("\n"+"\n")

config_detail = all_configs[optimized_cores[0]].get_attribute()
myFile.write( "Core_" + str(all_configs[optimized_cores[0]].get_coreID()) + ";Area:"  + str(all_configs[optimized_cores[0]].get_area()) + ";Peak_Power:" + str(all_configs[optimized_cores[0]].get_core_peak_power()) + ";h264ref_Power:" + str(all_configs[optimized_cores[0]].get_runtime_power(9)) + "\n")
myFile.write("F=" + str(all_configs[optimized_cores[0]].get_frequency()) + "-W=" + config_detail[0] + "-ROB=" + config_detail[1] + "-IQ=" + config_detail[2] + "-LQ=" + config_detail[3] + "-SQ=" + config_detail[4] + "-L1_I$=" + config_detail[5] + "-L1_D$=" + config_detail[6] + "-L2=" + config_detail[7] + "\n" + "\n")
myFile.close()

fileN = fileName + '.json'
myFile = open (fileN, 'w')
myFile.write("series: [{" + "\n")
myFile.write("  name: 'Largest_Core'," + "\n")
myFile.write("  data: [5,4,5,2,2,4],\n")
myFile.write("  pointPlacement: 'on'\n")
myFile.write("}\n")

config_detail = all_configs[optimized_cores[0]].get_attribute()

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

##Frequency
freq=all_configs[optimized_cores[0]].get_frequency()
if (freq==1.0):
    config_detail0=1
elif (freq==1.5):
    config_detail0=2
elif (freq==2.0):
    config_detail0=3
elif (freq==2.5):
    config_detail0=4
elif (freq==3.0):
    config_detail0=5
else:
    config_detail0=10000
##if (freq==1.0):
##    config_detail0=1
##elif (freq==1.25):
##    config_detail0=2
##elif (freq==1.5):
##    config_detail0=3
##elif (freq==1.75):
##    config_detail0=4
##elif (freq==2.0):
##    config_detail0=5
##elif (freq==2.25):
##    config_detail0=6
##elif (freq==2.5):
##    config_detail0=7
##elif (freq==2.75):
##    config_detail0=8
##elif (freq==3.0):
##    config_detail0=9
##else:
##    config_detail0=10000

myFile.write(" ,{name: 'core_" + str(all_configs[optimized_cores[0]].get_coreID()) + "'," + "\n")
myFile.write("  data: [" + str(config_detail0) + "," + str(config_detail[0]) + "," + str(config_detail1) + "," + str(config_detail2) + "," + str(config_detail3) + "," + str(config_detail4) + "]," +"\n")
myFile.write("  pointPlacement: 'on'\n")
myFile.write("}\n")
myFile.write("]\n")
myFile.close()

#### Printing out goodness, preferred core and core-ranking for each application #####
fileName += ".csv"
myFile = open (fileName, 'w')

for index in range(len(benchmark_list)):
    myFile.write(str(benchmark_map[index]) + ", config core" + str(all_configs[optimized_cores[0]].get_coreID()) + ", " + str(all_configs[optimized_cores[0]].get_perf(benchmark_list[index])) + ", " + str(all_configs[optimized_cores[0]].get_runtime_power(benchmark_list[index])) + ", " + str(all_configs[optimized_cores[0]].get_speedup(benchmark_list[index])))
    myFile.write("\n")
myFile.close()
