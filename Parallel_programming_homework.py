#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 18:38:46 2017

@author: kevin
"""
import matplotlib.pyplot as plt
num_processors = range(1,100)
proportions = [0.5, 0.67,  0.95, 0.99]
colors = ['r','b','g','k']
def speedup(p,n):#input proportion and number of processors
    speedup = []
    for processors in n:
        speedup.append(1/((1-p) + p/processors))#value of speed up
    return speedup

for idx, proportion in enumerate(proportions):
    plt.semilogx(num_processors,speedup(proportion,num_processors),label=str(proportion))
    
plt.legend(loc='upper right')