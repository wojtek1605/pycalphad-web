#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 17:42:11 2023

@author: wojtekgierlotka
"""

import os
import matplotlib.pyplot as plt
from pycalphad import Database, binplot
import pycalphad.variables as v

db_agal = Database('ag_al.TDB')
phases = ['LIQUID','FCC_A1']
fig = plt.figure(figsize=(9,6))
axes = fig.gca()
binplot(db_agal, ['AG', 'AL', 'VA'] , phases, {v.X('AL'):(0,1,0.02), v.T: (300, 1500, 10), v.P:101325, v.N: 1}, plot_kwargs={'ax': axes})

plt.show()