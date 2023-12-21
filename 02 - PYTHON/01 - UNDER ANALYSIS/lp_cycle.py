# -*- coding: utf-8 -*-

"--------------------------------------------------------------------"

"""
Created on Tue Dec 14 13:11:50 2023

@author: pmbarral
"""

"--------------------------------------------------------------------"

"""""
Application notes:

    Include demi water pump & condensate pump.
    Include head loss in entering the bfw tank.
    Include pipe loss in boiler outler pipe, demi water pipe, bfw pipe, bfw tk steam, condensate pipe, process steam
    Incorporate the pressure control vakve
    Incorporate combustion or boiler efficiency. Perhaps with a bus, to account for radiative losses.
    Add improvements in bd management.

"""""
"--------------------------------------------------------------------"

# Functions:

def export(__file__, results):
    """
    This function exports the results of the simulation to a text file, stored in the same directory as the Python script.

    Parameters:
    __file__ (str): The name of the file being executed.
    results (DataFrame): A dataframe containing the simulation results.

    Returns:
    None

    """
 
    import os

    path = os.path.dirname(os.path.abspath(__file__))

    text_file = os.path.join(path, 'results.txt')

    formatted_text = results.to_string(index=False, justify='left')

    with open(text_file, 'w') as file:
        file.write(formatted_text)

"--------------------------------------------------------------------"

# General code:
        
from tespy.networks import Network
from tespy.connections import (Connection, Ref)
from tespy.components import (CycleCloser, Pump, Splitter, Valve, Sink, Source, Merge, SimpleHeatExchanger, Drum)

"--------------------------------------------------------------------"

# Set up the system.

my_plant = Network(p_unit='bar', T_unit='C', h_unit='kJ / kg', s_unit='kJ / kgK', m_unit='t / h', iterinfo=False)

"--------------------------------------------------------------------"

# Parameters:

p_0 = 1.101325  # [bar(a)] - normal atm pressure
p_lp = 12 + p_0 # [bar(a)] - process steam pressure

diff_p_eco = 2 # [bar(a)] - economizer differential pressure

pr_eco = p_lp / (p_lp + diff_p_eco)

m_lp = 100 # [t/h] - process steam mass flow

t_tk = 105 # [C] - bfw tk temperature
t_dw = 25 # [C] - demi water temperature

t_cond = 70 # [C] - condensate return temperature
m_cond = 70 # [t/h] - condensate return mass flow

approach = 50 # [C] - economizer --> drum

purge = 0.05 # [dim] - softened water

"--------------------------------------------------------------------"

# Components

cc = CycleCloser('cycle closer')

fp = Pump('boiler feedwater pump', eta_s=0.7)

hd = Splitter('LP header')

cv = Valve('pressure control valve')

lpsi = Sink('industrial process')

cnrt = Source('condensate return')

mk = Source('demi water makeup')

tk = Merge('boiler feedwater tank', num_in=3)

ec = SimpleHeatExchanger('economizer', pr=pr_eco)

dr = Drum("drum")

ev = SimpleHeatExchanger("evaporator")

bd = Splitter('blowdown')

wst = Sink('waste')

"--------------------------------------------------------------------"

# Connections:

N = 14

c = [None] * N
names = [None] * N

names[0] = 'boiler outlet'
c[0] = Connection(dr, 'out2', cc, 'in1', label='0') # same state as c[1]

names[1] = 'boiler outlet'
c[1] = Connection(cc, 'out1', hd, 'in1', label='1')
c[1].set_attr(fluid={'water': 1}, m=Ref(c[0], 1, 0), p=p_lp)

names[2] = 'process steam'
c[2] = Connection(hd, 'out1', lpsi, 'in1', label='2')
c[2].set_attr(m=m_lp)

names[3] = 'tk steam'
c[3] = Connection(hd, 'out2', cv, 'in1', label='3')

names[4] = 'vlp tk steam'
c[4] = Connection(cv, 'out1', tk, 'in1', label='4')

names[5] = 'tk outlet'
c[5] = Connection(tk, 'out1', fp, 'in1', label='5')
c[5].set_attr(fluid={'water': 1}, T=t_tk, x=0)

names[6] = 'boiler fw'
c[6] = Connection(fp, 'out1', ec, 'in1', label='6')

names[7] = 'makeup water'
c[7] = Connection(mk, 'out1', tk, 'in2', label='7')
c[7].set_attr(T=t_dw, fluid={'water': 1})

names[8] = 'condensate return'
c[8] = Connection(cnrt, 'out1', tk, 'in3', label='8')
c[8].set_attr(fluid={'water': 1}, m=m_cond, T=t_cond)

names[9] = 'economizer outlet'
c[9] = Connection(ec, 'out1', dr, 'in1', label='9', Td_bp=-approach)

names[10] = 'drum water outlet'
c[10] = Connection(dr, 'out1', bd, 'in1', label='10')

names[11] = 'riser'
c[11] = Connection(ev, 'out1', dr, 'in2', label='11')
c[11].set_attr(x=0.05)

names[12] = 'blowdown'
c[12] = Connection(bd, 'out1', wst, 'in1', label='12')
c[12].set_attr(m=Ref(c[6], purge, 0))

names[13] = 'downcomer'
c[13] = Connection(bd, 'out2', ev, 'in1', label='13')

"--------------------------------------------------------------------"

# Processing:
for j in range(0,N):
    my_plant.add_conns(c[j])

my_plant.solve(mode='design')

"--------------------------------------------------------------------"

# Postprocessing:

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
results = results.round(3)

"--------------------------------------------------------------------"

# Exportation:
        
export(__file__, results)