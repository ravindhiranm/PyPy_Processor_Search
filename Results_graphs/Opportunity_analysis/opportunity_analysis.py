#!/usr/bin/python

##Shri Lakshmi Devi sametha Prahladhavaradhan
##Perundevi Sametha Devadhirajan
##Evulate the performance of a given configuration

import os
import math
import sys
import random
import itertools
import matplotlib.pyplot as plt
import brewer2mpl
import prettyplotlib as ppl
import numpy as np
from scipy import stats

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

mat_bpwlist = []
mat_bpw2list = []
mat_ipc = []
mat_extime = []
mat_power = []
mat_energy =[]
mat_edp =[]
mat_ed2p =[]

################ Printing BIPS/W details #################################
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)

fig, ax = plt.subplots(figsize=(18,6),dpi=400)

###Create markers
markers = itertools.cycle(('d','h',',','+', '.', 'o', '*', '^'))
##markers = itertools.cycle(('o', '*', '^'))

##Color Map
##set2 = brewer2mpl.get_map('Set1', 'qualitative',9).mpl_colors
##set2 = brewer2mpl.get_map('Paired', 'qualitative', len(benchmark_list)).mpl_colors


for index in range(len(benchmark_list)):
    bpw_list = []
    power_list =[]
    for i in range(0,3240):
        ##power_list.append(float(all_configs[i].get_core_peak_power()))
        power_list.append(float(all_configs[i].get_area()))
        bpw_list.append(bips_per_watt(all_configs[i].get_perf(benchmark_list[index]),float(all_configs[i].get_attribute()[0]), (float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power()))))
###	new_power_list = power_list
###	new_power_list.sort()
###	##bpw_list.sort()
###	new_bpw_list=bpw_list
###	for j in range(0,len(new_power_list)):
###		t = power_list.index(new_power_list[j])
###		new_bpw_list[j] = bpw_list[t]
    #ax.plot(range(0,3240),bpw_list, color=set2[index], label=benchmark_map[index], linewidth=0.75)
    ax.plot(range(0,3240),bpw_list, label=benchmark_map[index], marker = markers.next(), markersize=2, linewidth=1)
    ##ax.plot(new_power_list,new_bpw_list, color=set2[index], label=benchmark_map[index], marker = markers.next(), markersize=2, linewidth=1.5)

ax.set_ylabel('BIPS/W')
##ax.set_xlim(0, 672)
##plt.legend(loc=2)
plt.legend(loc=1)
fig.tight_layout()
fig.savefig('bipsw.png')
############################################################################

################ Printing EPI details #################################
fig, ax = plt.subplots(figsize=(18,6),dpi=400)

###Create markers
markers = itertools.cycle(('d','h',',','+', '.', 'o', '*', '^'))
##markers = itertools.cycle(('o', '*', '^'))

##Color Map
##set2 = brewer2mpl.get_map('Set1', 'qualitative',9).mpl_colors
##set2 = brewer2mpl.get_map('Paired', 'qualitative', len(benchmark_list)).mpl_colors


for index in range(len(benchmark_list)):
    epi_list = []
    core_area =[]
    for i in range(0,3240):
        epi_list.append(execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0]))*(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power()))/float(all_configs[i].get_icount(benchmark_list[index])))
        core_area.append(float(all_configs[i].get_area()))
    sorted_core_area = core_area
    sorted_core_area.sort()
    new_epi_list = epi_list
    for j in range(0,len(sorted_core_area)):
        t = core_area.index(sorted_core_area[j])
        new_epi_list[j] = epi_list[t]
    ax.plot(range(0,3240),epi_list, label=benchmark_map[index], marker = markers.next(), markersize=2, linewidth=1)
    ##ax.plot(sorted_core_area,new_epi_list, color=set2[index], label=benchmark_map[index], marker = markers.next(), markersize=2, linewidth=1.5)

ax.set_ylabel('EPI (J/Instrcution)')
#ax.set_xlabel('Core Area (mm^2)')
##ax.set_xlim(0, 672)
plt.legend(bench_list_text, ncol=9, loc='upper center',
        bbox_to_anchor=[0.5, 1.1],
        columnspacing=1.0, labelspacing=0.0,
        handletextpad=0.0, handlelength=1.5,
        fancybox=True, shadow=True)
fig.tight_layout()
fig.savefig('epi_config_sorted.png')
#fig.savefig('epi_sorted_core_area.png')
############################################################################
################ Printing EPI details #################################
fig, ax = plt.subplots(figsize=(18,6),dpi=400)

###Create markers
markers = itertools.cycle(('d','h',',','+', '.', 'o', '*', '^'))
##markers = itertools.cycle(('o', '*', '^'))

##Color Map
##set2 = brewer2mpl.get_map('Set1', 'qualitative',9).mpl_colors
##set2 = brewer2mpl.get_map('Paired', 'qualitative', len(benchmark_list)).mpl_colors


for index in range(len(benchmark_list)):
    epi_list = []
    peak_power =[]
    for i in range(0,3240):
        epi_list.append(execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0]))*(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power()))/float(all_configs[i].get_icount(benchmark_list[index])))
        peak_power.append(float(all_configs[i].get_core_peak_power()))
    sorted_peak_power = peak_power
    sorted_peak_power.sort()
    new_epi_list = epi_list
    for j in range(0,len(sorted_peak_power)):
        t = peak_power.index(sorted_peak_power[j])
        new_epi_list[j] = epi_list[t]
    ax.plot(sorted_peak_power,new_epi_list,label=benchmark_map[index], marker = markers.next(), markersize=2, linewidth=1.5)

ax.set_ylabel('EPI (J/Instrcution)')
ax.set_xlabel('Peak Power (W)')
##ax.set_xlim(0, 672)


plt.legend(bench_list_text, ncol=9, loc='upper center',
        bbox_to_anchor=[0.5, 1.1],
        columnspacing=1.0, labelspacing=0.0,
        handletextpad=0.0, handlelength=1.5,
        fancybox=True, shadow=True)
fig.tight_layout()
fig.savefig('epi_sorted_peak_power.png')
############################################################################
################## Printing BIPS^2/W details #################################
##for index in range(len(benchmark_list)):
##        bpw2_list = []
##	n_bpw2_list = []
##	for i in range(0,3240):
##                bpw2_list.append(bips_per_watt2(all_configs[i].get_perf(benchmark_list[index]),float(all_configs[i].get_attribute()[0]), (float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power()))))
##	value = max(bpw2_list)
##	n_bpw2_list = bpw2_list
##	for j in range(len(bpw2_list)):
##		n_bpw2_list[j] = bpw2_list[j]/value
##        mat_bpw2list.append(n_bpw2_list)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_bpw2list),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.tight_layout()
##fig.colorbar(p)
##fig.savefig('bips2w.png')
##############################################################################
##
################## Plotting execution time ###################################
##for index in range(len(benchmark_list)):
##        extime=[]
##        n_extime=[]
##	for i in range(0,3240):
##		extime.append(execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0])))
##	value = max(extime)
##	n_extime = extime
##	for j in range(len(extime)):
##		#n_extime[j] = value/extime[j]
##		n_extime[j] = extime[j]/value
##        mat_extime.append(n_extime)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_extime),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.tight_layout()
##fig.colorbar(p)
##fig.savefig('extime.png')
##############################################################################
##
################## Plotting Energy details ###################################
##for index in range(len(benchmark_list)):
##	energy=[]
##	n_energy=[]
##	for i in range(0,3240):
##                energy.append(execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0]))*(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power())))
##	value = max(energy)
##	n_energy = energy
##	for j in range(len(energy)):
##		#n_extime[j] = value/extime[j]
##		n_energy[j] = energy[j]/value
##	mat_energy.append(n_energy)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_energy),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.tight_layout()
##fig.colorbar(p)
##fig.savefig('energy.png')
##############################################################################
##
################## Plotting EDP details ######################################
##for index in range(len(benchmark_list)):
##	edp=[]
##	n_edp=[]
##	for i in range(0,3240):
##                edp.append((execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0]))**2)*(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power())))
##	value = max(edp)
##	n_edp = edp
##	for j in range(len(edp)):
##		#n_extime[j] = value/extime[j]
##		n_edp[j] = edp[j]/value
##	mat_edp.append(n_edp)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_edp),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.tight_layout()
##fig.colorbar(p)
##fig.savefig('edp.png')
##############################################################################
##
################## Plotting ED^2P details ######################################
##for index in range(len(benchmark_list)):
##	ed2p=[]
##	n_ed2p=[]
##	for i in range(0,3240):
##                ed2p.append((execution_time(all_configs[i].get_cycles(benchmark_list[index]),float(all_configs[i].get_attribute()[0]))**3)*(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power())))
##	value = max(ed2p)
##	n_ed2p = ed2p
##	for j in range(len(ed2p)):
##		#n_extime[j] = value/extime[j]
##		n_ed2p[j] = ed2p[j]/value
##	mat_ed2p.append(n_ed2p)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_ed2p),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.colorbar(p)
##fig.tight_layout()
##fig.savefig('ed2p.png')
##############################################################################
##
################## Plotting IPC details ######################################
##for index in range(len(benchmark_list)):
##	ipc=[]
##	n_ipc=[]
##	for i in range(0,3240):
##                ipc.append(float(all_configs[i].get_perf(benchmark_list[index])))
##	value = max(ipc)
##	n_ipc = ipc
##	for j in range(len(ipc)):
##		n_ipc[j] = ipc[j]/value
##	mat_ipc.append(n_ipc)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_ipc),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.tight_layout()
##fig.colorbar(p)
##fig.savefig('ipc.png')
##############################################################################
##
################## Plotting power details ######################################
##for index in range(len(benchmark_list)):
##        power=[]
##        n_power=[]
##	for i in range(0,3240):
##                power.append(float(all_configs[i].get_runtime_power(benchmark_list[index])) + float(all_configs[i].get_leak_power()))
##	value = max(power)
##	n_power = power
##	for j in range(len(power)):
##		n_power[j] = power[j]/value
##	mat_power.append(n_power)
##
##fig, ax = ppl.subplots(figsize=(18,6),dpi=400)
##p = ax.pcolormesh(np.array(mat_power),cmap=green_purple)
##ax.set_yticks(range(0,len(benchmark_list)))
##ax.set_yticklabels(benchmark_list)
##ax.set_xlim(0, 672)
##
##fig.tight_layout()
##fig.colorbar(p)
##fig.savefig('power.png')
##############################################################################
##
#################### Performance vs Power scatter plot #######################
##
### Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
####set2 = brewer2mpl.get_map('Paired', 'qualitative', len(benchmark_list)).mpl_colors
####fig, ax = plt.subplots(1)
####
##### Remove top and right axes lines ("spines")
####spines_to_remove = ['top', 'right']
####for spine in spines_to_remove:
####    ax.spines[spine].set_visible(False)
####
####for j in range(len( benchmark_list)):
####	for i in range(0,3240):
####		x = all_configs[i].get_perf(benchmark_list[j])
####		y = float(all_configs[i].get_runtime_power(benchmark_list[j])) + float(all_configs[i].get_leak_power())
####    		color = set2[j]
####    		ax.scatter(x, y, label=str(benchmark_list[j]), color=color)
####
##### Get rid of ticks. The position of the numbers is informative enough of
##### the position of the value.
####ax.xaxis.set_ticks_position('none')
####ax.yaxis.set_ticks_position('none')
####ax.set_xlabel('IPC')
####ax.set_ylabel('Runtime Power(W)')
######ax.legend()
####fig.tight_layout()
####
####fig.savefig('perf_v_power.png')
## #####################################################################################
#################### Performance vs Power scatter plot #######################
##
####num_plots = len(benchmark_list)
####n = int(math.ceil(math.sqrt(num_plots)))
####
##### Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
####set2 = brewer2mpl.get_map('set2', 'qualitative', 8).mpl_colors
####
####fig = plt.figure(figsize=(14,10))
####
##### Maximum value we see for fraction common bound
####xlim = [0,3.5]
##### Maximum value we see for alignment scores
####ylim = [0,4.5]
####
####axes = [plt.subplot(n,n,i) for i in range(1,num_plots+1)]
####
####for j in range(len( benchmark_list)):
####	for i in range(0,3240):
####		ax = axes[j]
####		x = all_configs[i].get_perf(benchmark_list[j])
####		y = float(all_configs[i].get_runtime_power(benchmark_list[j])) + float(all_configs[i].get_leak_power())
####    		color = set2[0]
####    		ax.scatter(x, y, label=str(benchmark_list[j]), color=color)
####		ax.set_ylim(ylim)
####    		ax.set_xlim(xlim)
####		#ax.xticks(list(np.arange(0,3.5,0.5)), size='small', rotation='vertical')
####
####		# Remove top and right axes and ticks
####		ax.spines['top'].set_visible(False)
####		ax.spines['right'].set_visible(False)
####		ax.yaxis.set_ticks_position('none')
####		ax.xaxis.set_ticks_position('none')
####
####		ax.set_title(benchmark_list[j])
####		ax.set_xlabel('IPC')
####		ax.set_ylabel('Runtime Power (W)')
####
####plt.tight_layout()
####fig.savefig('per_app_perf_v_power.png')
## #####################################################################################
#################### Performance vs Peak Power scatter plot #######################
##
####num_plots = len(benchmark_list)
####n = int(math.ceil(math.sqrt(num_plots)))
####
##### Get "Set2" colors from ColorBrewer (all colorbrewer scales: http://bl.ocks.org/mbostock/5577023)
####set2 = brewer2mpl.get_map('set2', 'qualitative', 8).mpl_colors
####
####fig = plt.figure(figsize=(14,10))
####
##### Maximum value we see for fraction common bound
####xlim = [0,3.5]
##### Maximum value we see for alignment scores
####ylim = [0,8]
####
####axes = [plt.subplot(n,n,i) for i in range(1,num_plots+1)]
####
####for j in range(len( benchmark_list)):
####	for i in range(0,3240):
####		ax = axes[j]
####		x = all_configs[i].get_perf(benchmark_list[j])
####		y = float(all_configs[i].get_app_peak_power(benchmark_list[j])) + float(all_configs[i].get_leak_power())
####    		color = set2[0]
####    		ax.scatter(x, y, label=str(benchmark_list[j]), color=color)
####		ax.set_ylim(ylim)
####    		ax.set_xlim(xlim)
####		#ax.xticks(list(np.arange(0,3.5,0.5)), size='small', rotation='vertical')
####
####		# Remove top and right axes and ticks
####		ax.spines['top'].set_visible(False)
####		ax.spines['right'].set_visible(False)
####		ax.yaxis.set_ticks_position('none')
####		ax.xaxis.set_ticks_position('none')
####
####		ax.set_title(benchmark_list[j])
####		ax.set_xlabel('IPC')
####		ax.set_ylabel('Runtime Power (W)')
####
####plt.tight_layout()
####fig.savefig('per_app_perf_v_peak_power.png')
## #####################################################################################
