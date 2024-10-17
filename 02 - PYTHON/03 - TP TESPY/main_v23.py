def export(__file__, results):
    """
    Esta función exporta los resultados de la simulación a un archivo de texto, almacenado en el mismo directorio que el script de Python.

    Parámetros:
    __file__ (str): El nombre del archivo que se está ejecutando.
    results (DataFrame): Un dataframe que contiene los resultados de la simulación.

    Retorna:
    Ninguno
    """
    # Se importa el módulo 'os' para trabajar con rutas de archivos y directorios.
    import os

    # Se obtiene la ruta completa del directorio donde está guardado el archivo Python.
    path = os.path.dirname(os.path.abspath(__file__))

    # Se crea la ruta completa del archivo de texto 'results.txt'.
    text_file = os.path.join(path, 'results.txt')

    # Se formatean los datos del DataFrame como una cadena de texto.
    # 'index=False' significa que no se incluye la columna de índices.
    # 'justify='left'' indica que el texto se alinea a la izquierda.
    formatted_text = results.to_string(index=False, justify='left')

    # Se abre el archivo 'results.txt' en modo de escritura ('w') y escribir los datos formateados
    with open(text_file, 'w') as file:
        file.write(formatted_text)




from tespy.networks import Network
from tespy.components import (
    CycleCloser, Turbine, Pump, Valve, Source, Sink, Splitter,
    Merge, SimpleHeatExchanger, HeatExchanger, Drum,
)
from tespy.connections import Bus, Connection, Ref

nw = Network()
nw.set_attr(
    T_unit='C',
    p_unit='bar',
    h_unit='kJ / kg',
    m_unit='t / h',
    s_unit='kJ / kgK',
    iterinfo=False
)

powergen = Bus("electrical power output")
nw.add_busses(powergen)

pamb = 1.013
Tamb = 17

cc = CycleCloser('cycle closer HPDRUM to ST')

st_ext = Turbine('extraction st', eta_s=0.9)
st_cond = Turbine('cond st', eta_s=0.9)

att_pump = Pump('att_pump', eta_s=0.7)
cond_pump = Pump('cond_pump', eta_s=0.7)
sg_pump = Pump('steam generator pump', eta_s=0.7)
lp_pump=Pump('low pressure pump', eta_s=0.7)

cond_st_cv = Valve('cond st cv', pr=0.85)

water_inlet_1 = Source('Process condensate return')
water_inlet_2 = Source('Water makeup')

turbine_exhaust = Source('Hot gases source')

wst = Sink('LPDRUM saturated steam waste')
wst_2 = Sink('HPDRUM saturated liquid waste')
process_steam = Sink('process IP steam')
gases_outlet = Sink('hot gases outlet')

sp_1 = Splitter('st inner splitter')
sp_2 = Splitter('condensate header')
sp_3 = Splitter('HPEC1 splitter')
sp_4 = Splitter('HPDRUM outlet')
bd_1 = Splitter('LPDRUM splitter to waste')
bd_2= Splitter('HPDRUM splitter to waste')

me_1 = Merge('Attemper')
me_3 = Merge('Water from reposition & condensate mixture', num_in=3)
me_4 = Merge('merge at the inlet of sweet water condenser in SG')
me_5 = Merge('attemp HPS2')

HE = HeatExchanger('heat exchanger', pr1=0.9, pr2=0.9)

LPEV1 = HeatExchanger('LPEV1', pr1=1)
# LPEV1 = SimpleHeatExchanger('LPEV1')

LPDRUM = Drum('LP Drum')

HPEC1 = HeatExchanger('HPEC1', pr1=1)
HPEC2 = HeatExchanger('HPEC2',pr1=1, pr2=1)
HPEC3 = HeatExchanger('HPEC3', pr1=1, pr2=1)
# HPEC1 = SimpleHeatExchanger('HPEC1')
# HPEC2 = SimpleHeatExchanger('HPEC2', pr=1)
# HPEC3 = SimpleHeatExchanger('HPEC3', pr=1)

HPEV1 = HeatExchanger('HPEV1', pr1=1)  # must be pr1
# HPEV1 = SimpleHeatExchanger('HPEV1')

HPS1 = HeatExchanger('HPS1', pr1=1)
# HPS1 = SimpleHeatExchanger('HPS1')
HPS2 = HeatExchanger('HPS2', pr1=1, pr2=1)
# HPS2 = SimpleHeatExchanger('HPS2', pr=1)

HPDRUM = Drum('HP Drum')

condenser = SimpleHeatExchanger('condenser', pr=1)

HE_cond = HeatExchanger('sweet water condenser', pr1=1, pr2=1)
# HE_cond = SimpleHeatExchanger('sweet water condenser', pr=1)

powergen.add_comps(
                    {"comp": st_ext, "char": 0.97, "base": "component"},
                    {"comp": st_cond, "char": 0.97, "base": "component"},
                    {"comp": att_pump, "char": 0.97, "base": "bus"},
                    {"comp": cond_pump, "char": 0.97, "base": "bus"},
                    # {"comp": sg_pump, "char": 0.97, "base": "bus"},
                    )

from tespy.connections import (Connection, Ref)

N = 49
c = [None] * N
names = [None] * N

# caudal_vapor_sobrecalentado = 2*102.3 # t/h
c[0] = Connection(HPS2, 'out2', st_ext, 'in1', label='1')
c[0].set_attr(
                #m=caudal_vapor_sobrecalentado,
                fluid={'water': 1}, T=480, p0=88.5
              )
names[0] = 'hp steam'

c[1] = Connection(st_ext, 'out1', sp_1, 'in1', label='2')
names[1] = 'extraction st outlet'

caudal_extraccion_turbina = 160 # t/h
c[2] = Connection(sp_1, 'out2', me_1, 'in2', label='3')
c[2].set_attr(m=caudal_extraccion_turbina)
names[2] = 'Steam from TV to attemp'

c[3] = Connection(sp_1, 'out1', cond_st_cv, 'in1', label='4')
names[3] = 'cond st cv inlet'

c[4] = Connection(cond_st_cv, 'out1', st_cond, 'in1', label='5')
names[4] = 'cond st inlet'

c[5] = Connection(st_cond, 'out1', condenser, 'in1', label='6')
names[5] = 'condenser inlet'

c[6] = Connection(condenser, 'out1', sp_2, 'in1', label='7')
c[6].set_attr(x=0, T=Tamb + 18)
names[6] = 'condenser outlet'

c[7] = Connection(sp_2, 'out1', cond_pump, 'in1', label='8')
names[7] = 'cond pump inlet'

c[8] = Connection(sp_2, 'out2', att_pump, 'in1', label='9')
names[8] = 'att pump inlet'

c[9] = Connection(att_pump,'out1', me_1,'in1',label='10')
names[9] = 'att pump outlet'

presion_vapor_proceso = 13 # bar(a)
grado_sobrecalentamiento = 10 # C
c[10] = Connection(me_1, 'out1',process_steam,'in1',label='11')
c[10].set_attr(
                Td_bp=grado_sobrecalentamiento,
                p=presion_vapor_proceso
                )
names[10] = 'process steam'

c[11] = Connection(cond_pump,'out1', me_3, 'in1', label='12')
c[11].set_attr(p=pamb)
names[11] = 'cond pump outlet'

retorno_condensado = 0.75 # dim
c[12] = Connection(water_inlet_1, 'out1', me_3, 'in2', label='13')
c[12].set_attr( m=Ref(c[10], retorno_condensado, 0), fluid={'water': 1}, x=0)
names[12] = 'Condensate return from process'

c[13] = Connection(water_inlet_2,'out1',me_3,'in3',label='14')
c[13].set_attr(T=Tamb, fluid={"water": 1})
names[13] = 'Water makeup'

c[14] = Connection(me_3,'out1', lp_pump,'in1', label='15')
names[14] = 'Water mixture feed to low pressure pump'

c[15] = Connection(lp_pump,'out1', HE,'in2', label='16')
c[15].set_attr(p=2.3, T=55)
names[15] = 'Water mixture feed to heat exchanger'

c[16] = Connection(HE,'out2', LPDRUM,'in1',label='17')
c[16].set_attr(T=100, p0=2.3)  # here p0 is required apparently
names[16] = 'heated water feed to LPDRUM'

c[17] = Connection(HE,'out1', sg_pump,'in1', label='18')
names[17] = 'Cooled water feed to HP pump'

c[18] = Connection(sg_pump, 'out1', sp_3,'in1', label='19')
c[18].set_attr(p=88.52)
names[18] = 'pressurized water to HPEC1'

c[19] = Connection(sp_3, 'out1', me_4, 'in2', label='20')
c[19].set_attr(m=0)
names[19] = 'pressurized water to sg condenser'

c[20] = Connection(sp_3, 'out2', HPEC1, 'in2', label='21')  # in2
names[20] = 'pressurized water to HPEC1'

c[21] = Connection(HPEC1, 'out2', HPEC2, 'in2', label='22')  # in2
c[21].set_attr(T=116.1, p0=88.52)  # starting value necessary apparently
names[21] = 'pressurized water to HPEC2'

c[22] = Connection(HPEC2, 'out2', me_4, 'in1', label='23')
c[22].set_attr(T=230.9, p0=88.52)  # same here
names[22] = 'outlet of HPEC2 to merge with cold flow'

c[23] = Connection(me_4, 'out1', HE_cond, 'in2', label='24')  # this should be in2
# c[23].set_attr(p0=88.52)  # this cannot be set here due to connection with sp_3
names[23] = 'outlet of merge to sweet water condenser'

c[24] = Connection(HE_cond, 'out2', HPEC3, 'in2', label='25')  # in2
c[24].set_attr()  # temperature for initial solution
names[24] = 'outlet of sweet water condenser to HPEC3'

c[25] = Connection(HPEC3, 'out2', HPDRUM, 'in1', label='26')
c[25].set_attr(T=289.9, p0=90)
names[25] = 'outlet of HPEC3 to HP drum'

c[26] = Connection(HPDRUM, 'out1', bd_2, 'in1', label='27')
names[26] = 'saturated liquid outlet of HPDRUM to Splitter'

c[27] = Connection(bd_2, 'out1', HPEV1, 'in2', label='28')  # in2
names[27] = 'saturated liquid outlet of HPDRUM to HPEV1'

c[28] = Connection(bd_2, 'out2', wst_2, 'in1', label='29')
names[28] = 'saturated liquid outlet of HPDRUM to waste'
c[28].set_attr(m=2)

c[29] = Connection(HPEV1, 'out2', HPDRUM, 'in2', label='30')
c[29].set_attr(x=0.05)
names[29] = 'saturated steam outlet of HPEV1 to HPDRUM'

c[30] = Connection(HPDRUM, 'out2', sp_4 , 'in1', label='31')
names[30] = 'saturated steam outlet of HPDRUM'

c[31] = Connection(sp_4, 'out1', HPS1, 'in2', label='32')  #  in2
names[31] = 'saturated steam inlet to HPS1'

c[32] = Connection(HPS1, 'out2', me_5, 'in1', label='33')
c[32].set_attr(T=528.6)
names[32] = 'Steam outlet of HPS1 to attemp'

c[33] = Connection(sp_4, 'out2', HE_cond, 'in1', label='34')
names[33] = 'Steam derivation of HPDRUM to sweet water condenser'

c[34] = Connection(HE_cond, 'out1', me_5, 'in2', label='35')
c[34].set_attr(x=0)
names[34] = 'Sweet water condenser outlet to attemp'

c[35] = Connection(me_5, 'out1', HPS2, 'in2', label='36')  # in 2!
c[35].set_attr(T=428.8)
names[35] = 'Attemp outlet to HPS2'

# c[36] = Connection(HPS2, 'out1', cc, 'in1', label='37')
# temperatura_vapor_sobrecalentado = 480 # C
# c[36].set_attr(T=temperatura_vapor_sobrecalentado)
# names[36] = 'Superheated steam to steam turbine'
# not actually required because you have make up water, that means no cc required

c[37] = Connection(LPDRUM,'out1', bd_1,'in1', label='38')
names[37] = 'Saturated liquid outlet of LPDRUM to LPEV1'

c[38] = Connection(bd_1, 'out1', HE, 'in1', label='39')
names[38] = 'LPDRUM saturated liquid outlet to HE'

c[39] = Connection(bd_1, 'out2', LPEV1, 'in2', label='40')
names[39] = 'Saturated liquid inlet to LPEV1'

c[40] = Connection(LPEV1, 'out2', LPDRUM, 'in2', label='41')
c[40].set_attr(x=0.05)
names[40] = 'Saturated steam inlet to LPDRUM'  # this is not actually saturated

c[41] = Connection(LPDRUM, 'out2', wst, 'in1', label='42')
names[41] = 'Saturated steam outlet to vent'
c[41].set_attr(m=2*0.05)

c[42] = Connection(turbine_exhaust, 'out1', HPS2, 'in1', label='43')
x_gh_CO2 = 0.061 # dim
x_gh_H2O = 0.07768 # dim
x_gh_N2 = 0.7364 # dim
x_gh_O2 = 0.1126 # dim
x_gh_Ar = 1 - x_gh_CO2 - x_gh_H2O - x_gh_N2 - x_gh_O2
T_gh = 712.9 # C
G_gh = 3*481.98 # t/h
p_gh = pamb # bar(a)
c[42].set_attr(
                m=G_gh,
                T=T_gh,
                p=p_gh,
                fluid={'O2': x_gh_O2, 'N2': x_gh_N2, 'CO2': x_gh_CO2, 'water': x_gh_H2O, 'Ar': x_gh_Ar}
                )
names[42] = 'Hot gases input to HPS2'

c[43] = Connection(HPS2, 'out1', HPS1, 'in1', label='44')
names[43] = 'Hot gases input to HPS1'

c[44] = Connection(HPS1, 'out1', HPEV1, 'in1', label='45')
names[44] = 'Hot gases input to HPEV1'

c[45] = Connection(HPEV1, 'out1', HPEC3, 'in1', label='46')
names[45] = 'Hot gases input to HPEC3'

c[46] = Connection(HPEC3, 'out1', HPEC2, 'in1', label='47')
names[46] = 'Hot gases input to HPEC2'

c[47] = Connection(HPEC2, 'out1', LPEV1 , 'in1', label='48')
names[47] = 'Hot gases input to LPEV1'

c[48] = Connection(LPEV1, 'out1', HPEC1 , 'in1', label='49')
names[48] = 'Hot gases input to HPEC1'

c[49] = Connection(HPEC1, 'out1', gases_outlet , 'in1', label='50')
names[49] = 'Hot gases outlet'

for j in range(0,N):
    if c[j] is not None:
        nw.add_conns(c[j])



nw.solve(mode='design')
nw.print_results()


# ***************************

# Sección 07: Postprocesado

bus_results = nw.results['electrical power output']
df_results_for_conns = nw.results['Connection']

# Se añade una nueva columna al DataFrame 'df_results_for_conns' llamada 'denomination'.
# Esta columna contiene los valores de la lista 'names'.
df_results_for_conns['denomination'] = names

# Se crea un nuevo DataFrame 'results' que contiene solo las columnas seleccionadas. El objetivo es contar con una visualización más cómoda que la que presenta la librería por default.
results = df_results_for_conns[['denomination',
                                'p','p_unit',
                                'T','T_unit',
                                'h','h_unit',
                                's','s_unit',
                                'x',
                                'm','m_unit']]

# Se Define el índice a partir del cual se encuentran los gases. Es decir, a partir del estado 42 (python es cero-indentado).
start_index_for_gases = 42

# Se crea un DataFrame 'results_gases' que contiene sólo las filas correspondientes a los gases y las columnas seleccionadas (sin la columna 'x').
results_gases = results[start_index_for_gases:]
results_gases = results_gases[['denomination',
                                'p','p_unit',
                                'T','T_unit',
                                'h','h_unit',
                                's','s_unit',
                                'm','m_unit']]

# Se actualiza el DataFrame 'results' para que solo contenga las filas antes de los gases.
results = results[0:start_index_for_gases]

# Se Elimina la primera fila del DataFrame 'results'.
results = results.drop(results.index[0])

# Se redondean todos los valores numéricos en el DataFrame 'results' a 3 decimales.
results = results.round(3)



# ***************************

# Sección 08: Exportación de resultados

# Para exportar los resultados a un archivo determinado, se utiliza la función declara en el inicio del script.       
export(__file__, results)