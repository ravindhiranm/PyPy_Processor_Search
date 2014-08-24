#!/usr/bin/python

##Sri Lakshmi Devi sametha Prahladhavaradhan
##Sri Perundevi Sametha Devadhirajan
##### Search for HeCMPs with all freq cores (statically assigned) ####

import math
import sys
import random
import itertools
import datetime

class Timer:
    def __enter__(self):
        self.start = datetime.datetime.now()
        return self

    def __exit__(self, *args):
        self.end = datetime.datetime.now()
        self.interval = (self.end - self.start).microseconds

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
        self.app_perf={}
        self.app_peak_power={}
        self.app_runtime_power={}
        self.app_cycles={}
        self.app_instructions={}
        self.app_bips2w={}

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

    ## BIPS^2/W for reducing evaluate time
    def set_bips2w (self, app, bips2w):
        self.app_bips2w[app] = bips2w

    def get_bips2w (self, app):
        return self.app_bips2w[app]


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

def choose_random_config (total_cores, area_constraint, power_constraint):
    ##Assign bogus high values
    processor_area = area_constraint+10
    processor_tdp = power_constraint+10
    total_core_range = range (0, total_cores)
    while (processor_area > area_constraint or processor_tdp > power_constraint):
        ##update statistics
        stats.update_searched()

        processor_area = 0.0
        processor_tdp = 0.0
        core=[]
        for i in total_core_range:
            core.append(all_configs[random.randrange(0,647)])
            processor_area += float(core[i].get_area())
            processor_tdp += float(core[i].get_core_peak_power())
    return core

def evaluate(total_cores, core, area_constraint, power_constraint):
    goodness_value_each_permutation=0.0
    permutations_goodness_container=[]
    workload_goodness_container=[]

    for p in workloads:
        permutations_goodness_container=[]
        for j in permute:
            goodness_value_each_permutation = 0.0
            for i in processor_size:
                goodness_value_each_permutation += core[i].get_bips2w(p[j[i]])
            permutations_goodness_container.append(goodness_value_each_permutation)
        workload_goodness_container.append(max(permutations_goodness_container))

    return sum(workload_goodness_container)/len(workload_goodness_container)

def exhaustive_search(total_cores,area_constraint, power_constraint):
    # overall best solution
    core_best = []
    avg_core_bips_best = 0.0

    for p in range(0, len(allowed_proc_configs)):
        ## Updating Statistics
        stats.update_evaluated()

        core_t=allowed_proc_configs[p]
        #with Timer() as t:
        avg_core_bips_t = evaluate (total_cores, core_t, area_constraint, power_constraint)

        #print('Request took %.03f microsecs.' % t.interval)

        if (avg_core_bips_t>avg_core_bips_best):
            core_best = core_t
            avg_core_bips_best = avg_core_bips_t

    return core_best

def simulated_annealing(total_cores,area_constraint, power_constraint):
    #Initial core choices
        core_i = choose_random_config (total_cores,area_constraint, power_constraint)
        avg_core_bips_i = evaluate (total_cores, core_i, area_constraint, power_constraint)

        # overall best solution
        core_best = core_i
        avg_core_bips_best = avg_core_bips_i

        quit=0
        T=10000000000
        while T>0:
            core_t=[]
            core_t = choose_random_config (total_cores,area_constraint, power_constraint)
            avg_core_bips_t = evaluate (total_cores, core_t, area_constraint, power_constraint)

            ### Keeps track of search space touched & when to quit
            stats.update_evaluated()
            quit=quit+1

            ## Calculate the current cost and the new cost
            p = float(math.exp(float(-(avg_core_bips_t-avg_core_bips_i)/T)))
            # Is it better, or does it make the probability cutoff?
            if (avg_core_bips_t>avg_core_bips_i or random.random()<p):
                core_i = core_t
                avg_core_bips_i = avg_core_bips_t

            if (avg_core_bips_t>avg_core_bips_best):
                core_best = core_t
                avg_core_bips_best = avg_core_bips_t
                quit=0 ## Reset if there is a change

            # Decrease the temperature
            #T=T*cool
            T=T-1

            if (quit < 1000000):
                continue
            elif (quit == 1000000):
                return core_best
            break
        print "Rama Rama Krishna Krishna"
        return core_best

############ Program Starts ########

## Assigning command-line  variables for human readability
input_file=sys.argv[1]
total_cores=int(sys.argv[2])
area_constraint=float(sys.argv[3])
power_constraint=float(sys.argv[4])

### Intializing class instances for all cores in the library ###
all_configs = [core_config() for i in range (0,648)]

#### Creating a dictionary to map benchmark names to numbers ####
benchmark_map={}
bench_map=0

for line in file (input_file):
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
    bips2w=bips_per_watt2(ipc,frequency,(float(runtime_dynamic)+float(total_leakage)))
    all_configs[r].set_bips2w(bench_map,float(bips2w))


#### to support legacy code - benchmark_list is used every where - see top of the program
benchmark_list = range(0,len(benchmark_map))

###Create multiprogrammed workload combinations to be used while evaluating goodness
workloads = list(itertools.combinations(benchmark_list,total_cores))

### Create indices for permutations of workloads
processor_size = range(0,total_cores)
permute = list(itertools.permutations(processor_size,total_cores))

### Setting the core peak power to the max observed peak power among applications
for i in xrange (0,648):
    peakPower=[]
    for index in range(0, len(benchmark_list)):
        current_benchmark = benchmark_list[index]
        peakPower.append(all_configs[i].get_app_peak_power(current_benchmark))
    all_configs[i].set_core_peak_power(max(peakPower))

###### Trying to precompute all cores that fit within constraints
allowed_proc_configs=[]
for core in itertools.combinations(all_configs,int(total_cores)):
    processor_area = 0.0
    processor_tdp = 0.0
    run_tdp=[]
    for i in range(0,len(core)):
        processor_area += core[i].get_area()
        processor_tdp += core[i].get_core_peak_power()

    if (processor_area < int(area_constraint) and processor_tdp < int(power_constraint)):
        allowed_proc_configs.append(list(core))

    if(total_cores == 2 or len(allowed_proc_configs) < 1500000):
        continue
    else:
        break

## Enabling statistics collection of the search
stats = statistics()
search_space_dimension = comb(len(all_configs),int(total_cores))

### Starting Search
optimized_cores = []
if (len(allowed_proc_configs) == 0):
    print "No valid HeCMP configurations found for given constraints. Loosen constraints and try again :)"
    sys.exit()

elif (total_cores == 2 or (len(allowed_proc_configs) > 0  and  len(allowed_proc_configs) < 1500000)):
    print "Starting Exhaustive Search: " + str(total_cores),str(area_constraint),str(power_constraint),str(len(allowed_proc_configs))
    optimized_cores=exhaustive_search(total_cores,area_constraint,power_constraint)
    all_considered = search_space_dimension
    search_space_touched=100

else:
    print "Starting Simulated Annealing Search: " + str(total_cores),str(area_constraint),str(power_constraint),str(len(allowed_proc_configs))
    optimized_cores=simulated_annealing(total_cores,area_constraint,power_constraint)
    all_considered = stats.return_searched()
    search_space_touched=float(all_considered)/search_space_dimension

## Goodness of the final chose core
bestcore_speedup = evaluate (int(total_cores), optimized_cores, float(area_constraint), float(power_constraint))

#### Printing out chosen core and search details to File
fileName = 'HeCMP_' + str(total_cores) + 'C_' + str(int(area_constraint)) + 'mm_' + str(int(power_constraint)) + 'W'
myFile = open (fileName, 'w')
myFile.write("########### SRI #########\n")
myFile.write("Total Search Space (" + str(len(all_configs)) + "choose" + str(int(total_cores)) + "): " + str(search_space_dimension) + "\n")
myFile.write("Allowed Processor Configs: " + str(len(allowed_proc_configs)) + "\n")
myFile.write("Search Space touched: " + str(all_considered) + " (" + str(search_space_touched) + "%)\n")
myFile.write("Constraint satisfying procs evaluated: " + str(stats.return_evaluated()) + "\n")
myFile.write("\n")
myFile.write("Average BIPS^2/W: " + str(bestcore_speedup))
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
myFile.write("  data: [5,4,7,3,3,4],\n")
myFile.write("  pointPlacement: 'on'\n")
myFile.write("}\n")

for i in range (0, len(optimized_cores)):
    config_detail = optimized_cores[i].get_attribute()

    ####attributes=[ss_width,rob_size,iq_size,lq_size,sq_size,l1_icache_size,l1_dcache_size,l2_cache_size]
    ##Check ROB Size to Determine Inorder of OoO
    if (int(config_detail[1])==1):
        config_detail1 = 1
    elif (int(config_detail[1])==32):
        config_detail1=2
    elif (int(config_detail[1])==48):
        config_detail1=3
    elif (int(config_detail[1])==48):
        config_detail1=4
    elif (int(config_detail[1])==128):
        config_detail1=5
    elif (int(config_detail[1])==168):
        config_detail1=6
    elif (int(config_detail[1])==192):
        config_detail1=7
    else:
        config_detail1=10000

    ##L1 I$
    if (int(config_detail[5])==16):
        config_detail2=1
    elif (int(config_detail[5])==32):
        config_detail2=2
    elif (int(config_detail[5])==64):
        config_detail2=3
    else:
        config_detail2=10000

    ##L1 D$
    if (int(config_detail[6])==16):
        (config_detail3)=1
    if (int(config_detail[6])==32):
        (config_detail3)=2
    elif (int(config_detail[6])==64):
        (config_detail3)=2
    else:
        config_detail2=10000

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
    freq=optimized_cores[i].get_frequency()
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

    myFile.write(" ,{name: 'core_" + str(optimized_cores[i].get_coreID()) + "'," + "\n")
    myFile.write("  data: [" + str(config_detail0) + "," + str(config_detail[0]) + "," + str(config_detail1) + "," + str(config_detail2) + "," + str(config_detail3) + "," + str(config_detail4) + "]," +"\n")
    myFile.write("  pointPlacement: 'on'\n")
    myFile.write("}\n")
myFile.write("]\n")
myFile.close()

#### Printing out goodness, preferred core and core-ranking for each application #####
fileName += ".csv"
myFile = open (fileName, 'w')

for index in range(len(benchmark_list)):
    for i in range (0, len(optimized_cores)):
        myFile.write(str(benchmark_map[index]) + ", config core" + str(optimized_cores[i].get_coreID()) + ", " + str(optimized_cores[i].get_perf(benchmark_list[index])) + ", " + str(optimized_cores[i].get_runtime_power(benchmark_list[index])) + ", " + str(optimized_cores[i].get_bips2w(benchmark_list[index])))
        myFile.write("\n")
myFile.close()
