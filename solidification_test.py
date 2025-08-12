#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 16:52:35 2025

@author: wojtekgierlotka
"""

import matplotlib.pyplot as plt
from pycalphad import Database, variables as v
from scheil import simulate_scheil_solidification

dbf = Database('ag_al.TDB')
comps = ['AG','AL','VA']
phases = sorted(dbf.phases.keys())
liquid_phase_name = 'LIQUID'
composition = input('Composition of simulation: ')
initial_composition = {v.X('AL'):float(composition)}
start_temperature = int(input('Starting temperature: '))

#sol_res1 = simulate_scheil_solidification(dbf, comps, phases, initial_composition, start_temperature)
sol_res = simulate_scheil_solidification(dbf,comps,phases,initial_composition, start_temperature, step_temperature=1)

for phase_name, amounts in sol_res.cum_phase_amounts.items():
    plt.plot(sol_res.temperatures, amounts, label=phase_name)
plt.plot(sol_res.temperatures, sol_res.fraction_liquid, label='LIQUID')
plt.ylabel('Phase Fraction')
plt.xlabel('Temperature (K)')
plt.title('Ag-20Al Scheil simulation, phase fractions')
plt.legend(loc='best')
plt.show()
