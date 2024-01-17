# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:14:50 2023

@author: pmbarral
"""

# Application notes:

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import (CycleCloser, SimpleHeatExchanger, Pump, Splitter, Valve, Sink, Source, Merge, Drum)

import os
import pandas as pd

my_plant = Network()
my_plant.set_attr(T_unit='C',p_unit='bar', h_unit='kJ / kg', m_unit='t / h', s_unit='kJ / kgK', iterinfo=False)

# Components
cc = CycleCloser('cycle closer')

fp = Pump('boiler feedwater pump')
fp.set_attr(eta_s=0.7)

hd = Splitter('LP header')

cv = Valve('pressure control valve')

lpsi = Sink('industrial process')

cnrt = Source('condensate return')

mk = Source('demi water makeup')

tk = Merge('boiler feedwater tank', num_in=3)

ec = SimpleHeatExchanger('economizer')
ec.set_attr(pr=1)

dr = Drum("drum")

ev = SimpleHeatExchanger("evaporator")

bd = Splitter('blowdown')

wst = Sink('waste')

# Connections

c = [None] * 14
names = [None] * 14

c[0] = Connection(dr, 'out2', cc, 'in1', label='0') # same state as c[1]
names[0] = 'boiler outlet'

c[1] = Connection(cc, 'out1', hd, 'in1', label='1') # boiler outlet
c[1].set_attr(p=13, fluid={'water': 1})
names[1] = 'boiler outlet'

from tespy.connections import Ref
c[0].set_attr(m=Ref(c[1], 1, 0))

c[2] = Connection(hd, 'out1', lpsi, 'in1', label='2') # process steam
c[2].set_attr(m=100)
names[2] = 'process steam'

c[3] = Connection(hd, 'out2', cv, 'in1', label='3') # tk steam
names[3] = 'tk steam'

c[4] = Connection(cv, 'out1', tk, 'in1', label='4') # vlp tk steam
names[4] = 'vlp tk steam'

c[5] = Connection(tk, 'out1', fp, 'in1', label='5') # tk outlet
c[5].set_attr(T=105, x=0, fluid={'water': 1})
names[5] = 'tk outlet'

c[6] = Connection(fp, 'out1', ec, 'in1', label='6') # boiler fw
names[6] = 'boiler fw'

c[7] = Connection(mk, 'out1', tk, 'in2', label='7') # makeup water
c[7].set_attr(T=25, fluid={'water': 1})
names[7] = 'makeup water'

c[8] = Connection(cnrt, 'out1', tk, 'in3', label='8') # condensate return
c[8].set_attr(T=70, m=70, fluid={'water': 1})
names[8] = 'condensate return'

c[9] = Connection(ec, 'out1', dr, 'in1', label='9') # economizer outlet
names[9] = 'economizer outlet'
c[9].set_attr(Td_bp=-50)

c[10] = Connection(dr, 'out1', bd, 'in1', label='10') # drum water outlet
names[10] = 'drum water outlet'

c[11] = Connection(ev, 'out1', dr, 'in2', label='11') # riser
c[11].set_attr(x=0.05)
names[11] = 'riser'

c[12] = Connection(bd, 'out1', wst, 'in1', label='12') # blowdown
names[12] = 'blowdown'
c[12].set_attr(m=Ref(c[6], 0.05, 0))

c[13] = Connection(bd, 'out2', ev, 'in1', label='13') # downcomer
names[13] = 'downcomer'

for j in range(0,14):
    my_plant.add_conns(c[j])

my_plant.solve(mode='design')

df_results_for_conns = my_plant.results['Connection']
df_results_for_conns['denomination'] = names

results = df_results_for_conns[['denomination',
                                'p','p_unit',
                                'T','T_unit',
                                'h','h_unit',
                                's','s_unit',
                                'x',
                                'm','m_unit']]

results = results.drop(results.index[0])

def print_results(file_path: str, results: pd.DataFrame) -> None:
    """
    Prints the results to a text file.

    Args:
        file_path (str): The path of the input file.
        results (pd.DataFrame): The results to be printed.
    """
    # Round the results to 3 decimal places
    results = results.round(3)

    # Get the directory of the input file
    directory = os.path.dirname(os.path.abspath(file_path))

    # Create the output file path
    output_file = os.path.join(directory, 'archivo.txt')

    # Format the results as a string
    formatted_text = results.to_string(index=False, justify='left')

    # Write the formatted results to the output file
    with open(output_file, 'w') as file:
        file.write(formatted_text)

print_results(__file__, results)