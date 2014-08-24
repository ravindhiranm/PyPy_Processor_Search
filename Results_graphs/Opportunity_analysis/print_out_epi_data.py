#!/usr/bin/python

##Shri Lakshmi Devi sametha Prahladhavaradhan
##Perundevi Sametha Devadhirajan
##Evulate the performance of a given configuration

import sys

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

###############################################################################

all_configs = [core_config() for i in range (0,3240)]

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
bench_list_text =[]
for index in benchmark_list:
    bench_list_text.append(benchmark_map[index])

### Setting the core peak power to the max observed peak power among applications
for i in xrange (0,3240):
    peakPower=[]
    for index in benchmark_list:
        peakPower.append(all_configs[i].get_app_peak_power(index))
    all_configs[i].set_core_peak_power(max(peakPower))

############################################################################

################ Printing EPI details #################################
for i in range(0,3240):
    print(str(i)),
    for index in benchmark_list:
         #benchmark_map[index]
         print (str((execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0]))*(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power()))/float(all_configs[i].get_icount(benchmark_list[index]))))),
    print " "
for index in benchmark_list:
    print benchmark_map[index],
############################################################################
