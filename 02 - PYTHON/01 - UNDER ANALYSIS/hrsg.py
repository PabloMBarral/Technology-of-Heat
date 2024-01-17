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

# dar dos txts, uno para los gases y otro para el agua vapor
# generar un plot con matplotlib, que ponga el exhausto, y luego a partir de la postcombustion que genere una spline
# darle un aspecto lindo al grafico con matplotlib
# poner pinch y approach con el minimo


from tespy.networks import Network
from tespy.connections import Connection
from tespy.components import SimpleHeatExchanger, Source, Sink

hrsg = Network(p_unit='bar', T_unit='C', h_unit='kJ / kg', s_unit='kJ / kgK', m_unit='kg / s', iterinfo=False)

x_gh_CO2 = 0.061
x_gh_H2O = 0.07768
x_gh_N2 = 0.7364
x_gh_O2 = 0.1126
x_gh_Ar = 1 - x_gh_CO2 - x_gh_H2O - x_gh_N2 - x_gh_O2

exhaust_gases = {"Ar": x_gh_Ar, "N2": x_gh_N2, "CO2": x_gh_CO2, "O2": x_gh_O2, "H2O": x_gh_H2O}

G_dot_gh = 500 # [tonne/h]
G_dot_gh = G_dot_gh / 3.6 # [kg/s]
t_g = 560 # [C]
p_0 = 1.01325 # [bar(a)]

lhv_ng = 8400 # [kcal/m3S]

V_dot_pc = 1000 # [m^3/h]

Q_dot_pc = lhv_ng * V_dot_pc * 4.1868 / 3600 # [kW]


pc = SimpleHeatExchanger("supplemental firing")
pc.set_attr(Q=Q_dot_pc * 1000) # Apparently, heat needs to be set in W

ex = Source("gt exhaust")

st = Sink("stack")

# Connections:

N = 2

c = [None] * N
names = [None] * N

names[0] = 'gt exhaust'
c[0] = Connection(ex, 'out1', pc, 'in1', label='0')
c[0].set_attr(T=t_g,p=p_0)

names[1] = 'stack'
c[1] = Connection(pc, 'out1', st, 'in1', label='1')
c[1].set_attr(fluid=exhaust_gases, m=G_dot_gh, p=p_0)



t_hp = 480 # [C]
p_hp = 66 # [bar(a)]


"--------------------------------------------------------------------"

# Processing:
for j in range(0,N):
    hrsg.add_conns(c[j])

hrsg.solve(mode='design')

"--------------------------------------------------------------------"

# Postprocessing:

df_results_for_conns = hrsg.results['Connection']
df_results_for_conns['denomination'] = names

results = df_results_for_conns[['denomination',
                                'p','p_unit',
                                'T','T_unit',
                                'h','h_unit',
                                's','s_unit',
                                'x',
                                'm','m_unit']]

# results = results.drop(results.index[0])
results = results.round(3)

"--------------------------------------------------------------------"

# Exportation:
        
export(__file__, results)
