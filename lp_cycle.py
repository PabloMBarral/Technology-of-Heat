# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:14:50 2023

@author: pmbarral
"""

# Application notes:
# TBD: boiler blowdown (use Drum + Evaporator (HeatExchanger)).

from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import (CycleCloser, SimpleHeatExchanger, Pump, Splitter, Valve, Sink, Source, Merge)

my_plant = Network()
my_plant.set_attr(T_unit='C',p_unit='bar', h_unit='kJ / kg', m_unit='t / h', s_unit='kJ / kgK', iterinfo=False)

# Components
cc = CycleCloser('cycle closer')
sg = SimpleHeatExchanger('steam generator') # needs improving when stating BD
sg.set_attr(pr=1)

fp = Pump('boiler feedwater pump')
fp.set_attr(eta_s=0.7)

hd = Splitter('LP header')
cv = Valve('pressure control valve')

lpsi = Sink('industrial process')

cnrt = Source('condensate return')

mk = Source('demi water makeup')

tk = Merge('boiler feedwater tank', num_in=3)
#tk.component()

# Connections

c = [None] * 9
names = [None] * 9

c[0] = Connection(sg, 'out1', cc, 'in1', label='0') # same state as c[1]
names[0] = 'boiler outlet'

c[1] = Connection(cc, 'out1', hd, 'in1', label='1') # boiler outlet
c[1].set_attr(p=13, x=1, fluid={'water': 1})
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

c[6] = Connection(fp, 'out1', sg, 'in1', label='6') # boiler fw
names[6] = 'boiler fw'

c[7] = Connection(mk, 'out1', tk, 'in2', label='7') # makeup water
c[7].set_attr(T=25, fluid={'water': 1})
names[7] = 'makeup water'

c[8] = Connection(cnrt, 'out1', tk, 'in3', label='8') # condensate return
c[8].set_attr(T=70, m=70, fluid={'water': 1})
names[8] = 'condensate return'

for j in range(0,9):
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

def impresion(__file__, results):
    results = results.round(3)

    import os

    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    archivo_texto = os.path.join(directorio_actual, 'archivo.txt')

    texto_formateado = results.to_string(index=False, justify='left')

    with open(archivo_texto, 'w') as file:
        file.write(texto_formateado)

impresion(__file__, results)

texto_formateado = results.to_string(index=False, justify='left')

with open(archivo_texto, 'w') as file:
    file.write(texto_formateado)
