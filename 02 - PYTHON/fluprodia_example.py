from fluprodia import FluidPropertyDiagram
import matplotlib.pyplot as plt
import numpy as np

diagram = FluidPropertyDiagram(fluid='H2O')
diagram.set_unit_system(T='°C', h='kJ/kg', p='bar',  s='kJ/kgK')

Q = np.linspace(0, 1, 11)
T = np.arange(25, 501, 25)
p = np.geomspace(0.01, 1000, 6) * 1e5
v = np.geomspace(0.001, 10, 5)
s = np.linspace(1.000, 10.000, 1)
h = np.linspace(0, 3600, 19)

diagram.set_isolines(Q=Q, T=T, p=p, v=v, s=s, h=h)
diagram.calc_isolines()

fig, ax = plt.subplots(1, figsize=(8, 5))
diagram.draw_isolines(diagram_type='logph', fig=fig, ax=ax, x_min=0, x_max=3000, y_min=0.01, y_max=1000)
plt.tight_layout()
fig.savefig('logph_diagram_H2O.svg')
fig.savefig('logph_diagram_H2O.png', dpi=300)


fig, ax = plt.subplots(1, figsize=(8, 5))
diagram.draw_isolines(diagram_type='Ts', fig=fig, ax=ax, x_min=0, x_max=8.000, y_min=0, y_max=700)
plt.tight_layout()
fig.savefig('Ts_diagram_H2O.svg')
fig.savefig('Ts_diagram_H2O.png', dpi=300)