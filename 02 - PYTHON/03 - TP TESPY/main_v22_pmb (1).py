"""
Comentarios generales:
    
    1. Colocar una bomba luego del tanque de mezcla.
    2. Corregir el domo de baja presióm.
    3. Dibujar el PFD como corresponde, colocando un tanque.
    4. Sistematizaría un poco la notación, pondría todo el código en minúsculas.
    5. Hacer una lista de estados, y una lista de componentes.
    6. Hacer un detalle de los estados que no se ven en el PFD (por ejemplo, el 1 -no es exactamente el CC, eso habría que detallarlo mejor, el 2 y el 3, o el 4 y el 5). Quizás convenga escribir en el PFD el tag de cada equipo.
    7. Cambié dónd especificamos la presión de 13 bar(a) de la extracción (es en el vapor de proceso). Intenté hacerlo con el caudal de 130 t/h pero me tira error. Tendríamos que verlo un cachito. Cambié la forma de especificar el vapor de proceso como 10C por encima de la saturación.
    8. Ojo con mezclar inglés y español.
    9. No veo la conveniencia de especificar 4 y 5, eso es posible englobarlo dentro del rendimiento isoentrópico. Por otra parte, no es consistente con la entrada de la turbina de alta presión, ya que allí hay también una válvula de control.
    10. Moví la definición de la caída de presión de la válvula de control de las ruedas MP y BP de la TV a la válvula, en lugar de tenerla en el estado. Creo que es más una propiedad del componente que del estado.
    11. Puse la definición de caída de presión en el condensador en el componente.
    12. Es posible usar el componente condensador. Si llegamos a tiempo, lo agregamos, aunque no sé si vale la pena. Sí haría la aclaración en el texto. Le cambié la definición: le puse temperatura y no presión.
    13. Relacioné la temperatura del agua de reposición y la del condensador con la temperatura ambiente.
    14. Puse algún rendimiento isoentrópico de una bomba, que estaba en 0.9, y lo pasé a 0.7.
    15. Eliminé las fuentes y sumideros de prueba, que no se usen.
    16. Quizás haya que renombrar al bus powergen, porque no queda claro qué es.
    17. Está raro el tema de los caudales: la reposición no debería ser un dato. Esto conviene que lo revisemos.
    18. En la mezcla de condensados (proceso y TV) estamos indicando una sola presión. Esto debe ser por el componente "merge". En caso de que así sea, no hay problemas, pero indiquémoslo. Esta presión se destruye en el tanque de mezcla. Veamos si le podemos indicar al tanque que su succión está a presión atmosférica.
    19. Cambié la composición y ajusté los parámetros de los gases húmedos. La presión no era correcta.
    20. Merge acepta varias entradas. Deberíamos poner un único merge en el tanque. Los otros están bien. Eventualmente, o podemos poner que las bombas de condensado, agua demi y condensado de proceso presurizan a una x presión y luego ponemos una bomba, o si no, sabiendo que subestimamos la potencia de esas bombas, hacemos que bombeen a presión atmosférica. Y la que luego presuriza al nivel del domo de baja presión es la bomba a pie del tanque de mezcla.
    21. La pérdida de carga en la HRSG totaliza unos 20 mbar, aprox. Es bastante poco. Es una valor que le especificas al calderista. No haríamos mal en desestimar la variación, ya que para los gases ideales como el modelo que usa tespy, la entalpía no depende de la presión. Sí tendríamos alguna variación en la exergía, pero mínima.
    22. Capaz que por una cuestión de claridad, movería la parte de análisis exergético para el final. Pero tenemos que verlo.
    23. El domo de baja presión no se purga. Los sólidos se van con el agua que va para el domo de alta presión. Ese sí se purga, porque no tiene ninguna salida de líquido.
    24. El estado 41 no lo encontré en el plano, no entendí bien cuál es.

Agregué comentarios, separé el código en secciones. Traté de poner espacios entre signos/variables para incrementar la legibilidad.

PMB - 2024-08-09
"""
# ***************************

# Sección -01: Preámbulo

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

# ***************************

# Sección 00: Invocaciones

# Invocamos el objeto "Network" ("Red"), para poder utilizarlo.
from tespy.networks import Network

# Invocamos los componentes de la red que necesitamos, para poder utiizarlos.
from tespy.components import (
                            CycleCloser,         # Este componente es un requerimiento de la librería para poder resolver un ciclo cerrado (en donde, por el propío cierre, sobra una ecuación de balance de masa: hay número de balances de masa requeridos menor -en una unidad- que el número de componentes)
                              
                            Turbine,
                            Pump,
                            Valve,

                            Source,              # Este es una fuente, que provee un fluido en las condiciones que se especifiquen.
                            Sink,                # Este es un sumidero, que absorbe un fluido en las condiciones que se especifiquen.  
                              
                            Splitter,            # Esto es un divisor: toma un caudal de un fluido y lo divide en muchas ramas, cada una con las mismas condiciones que la entrada.
                            Merge,               # Esto es una fusión, una mezcla: realiza el balance de masas y de energía.
                              
                               
                            SimpleHeatExchanger, # Esto es un intercambiado de calor modelizándolo de manera simplificada.                         
                            HeatExchanger,       # Esto es un intercambiado de calor modelizándolo de manera completa.
                              
                            Drum,
                            )

# Invocamos el objeto "Bus" (el cual representa a los flujos de potencia térmica o eléctrica/mecánica), para poder utilizarlo.
from tespy.connections import Bus

# Invocamos la herramienta de análisis exergético, para poder utilizarlo.
from tespy.tools import ExergyAnalysis

# ***************************

# Sección 02: Definición de atributos de la planta

# Una vez invocado el objeto (habilitado para su uso), debemos generar una variable que lo contenga. Es decir, efectivamente usarlo, generar el mecanismo para que pueda interactuar en el script.
my_plant = Network()

# Especificamos algunos atributos de la planta. Por ejemplo, el sistema de unidades. Asimismo, le solicitamos que no muestre información acerca de la iteración, para no ensuciar la salida del script.
# bar es bar(a).
my_plant.set_attr(
                T_unit='C',
                p_unit='bar', 
                h_unit='kJ / kg', 
                m_unit='t / h', 
                s_unit='kJ / kgK', 
                iterinfo=False
                )

# Una vez invocado el objeto (habilitado para su uso), generamos una variable que lo contenga. En este caso, generamos el bus "salida de potencia eléctrica (de la planta)". Este objeto se incorpora a la planta
powergen = Bus("electrical power output")
my_plant.add_busses(powergen)

"Quizás haya que renombrar al bus, porque no queda claro qué es físicamente."

# Parámetros globales
pamb = 1.013 # bar(a)
Tamb = 17 # C

# ***************************

# Sección 03: Especificación de componentes

cc = CycleCloser('cycle closer HPDRUM to ST')   # Cerrador de ciclo: entre la salida de vapor sobrecalentado y la entrada de la turbina de vapor (a las ruedas de alta presión).
cc_1 = CycleCloser('cycle closer LPDRUM to HE')

st_ext = Turbine('extraction st', eta_s=0.9)    # Ruedas de alta presión -entre entrada y extracción. Se indica el rendimiento isoentrópico de la etapa.
st_cond = Turbine('cond st', eta_s=0.9)         # Ruedas de media y baja presión a condensación. Se indica el rendimiento isoentrópico de la etapa.

att_pump = Pump('att_pump', eta_s=0.7)
cond_pump = Pump('cond_pump', eta_s=0.7)
sg_pump = Pump('steam generator pump', eta_s=0.7)
lp_pump=Pump('low pressure pump', eta_s=0.7)

cond_st_cv = Valve('cond st cv', pr=0.85)

water_inlet_1 = Source('Process condensate return')
water_inlet_2 = Source('Water makeup')
water_inlet_3 = Source('Water from boiler to HE')
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
me_2 = Merge('St condensate & process condensate return')
me_3 = Merge('Water from reposition & condensate mixture', num_in=3)
me_4 = Merge('merge at the inlet of sweet water condenser in SG')
me_5 = Merge('attemp HPS2')

# HE_aux = SimpleHeatExchanger('HE aux', pr=1)
HE = HeatExchanger('heat exchanger', pr1=0.9, pr2=0.9)

# LPEV1 = SimpleHeatExchanger('LPEV1')
# LPEV1_gases = SimpleHeatExchanger('LPEV1_gases', Q=-5550000, pr=1)
LPEV1 = HeatExchanger('LPEV1', pr2=1)



LPDRUM = Drum('LP Drum')

HPEC1 = HeatExchanger('HPEC1', pr1=1, pr2=1)
HPEC2 = HeatExchanger('HPEC2',pr1=1)
HPEC3 = HeatExchanger('HPEC3',pr1=1, pr2=1)

# HPEV1 = SimpleHeatExchanger('HPEV1')
# HPEV1_gases = SimpleHeatExchanger('HPEV1_gases',Q=-3850000, pr=1)
HPEV1 = HeatExchanger('HPEV1', pr2=1)


HPS1 = HeatExchanger('HPS1', Q=-10937000, pr1=1)
HPS2 = HeatExchanger('HPS2', pr1=1, pr2=1)

HPDRUM = Drum('HP Drum')

condenser = SimpleHeatExchanger('condenser', pr=1)
HE_cond = HeatExchanger('sweet water condenser', pr1=1, pr2=1)

# Se añaden los flujos de potencia eléctrica al bus general de la planta ("powergen").
# "char" representa la curva característica del rendimiento eléctrico del componente ("comp").
# "base" indica la componente base. Por ejemplo, que las ruedas de alta presión de la turbina sean "base" significa que la potencia surge de este componente (en forma mecánica) y se suma al bus, luego de aplicarle un rendimiento dado por "char".
# En este sentido, el "bus" puede interpretarse como una barra general del tablero general de la planta, a la cual acometen las máquinas generadoras y de la cual se toman los consumos.
powergen.add_comps(
                    {"comp": st_ext, "char": 0.97, "base": "component"},
                    {"comp": st_cond, "char": 0.97, "base": "component"},
                    {"comp": att_pump, "char": 0.97, "base": "bus"},
                    {"comp": cond_pump, "char": 0.97, "base": "bus"},
                    {"comp": sg_pump, "char": 0.97, "base": "bus"},
                    )

# ***************************

# Sección 04: Especificación de conexiones
# Parte A: Lado agua-vapor

from tespy.connections import (Connection, Ref)

#Probando nuevos valores

# Generamos dos listas vacías, que luego llenaremos con las conexiones y con sus descripciones ("names", nombres). names es una lista de strings.
# c es una lista de objetos propios de la librería tespy: las conexiones ("Connection"). Estas conexiones son flujos de materia, que tienen un estado termodinámico. Son lo que, coloquialmente, conocemos como "estados".
# El tamaño de ambas listas es N. Es decir, el índice de cada una las recorre desde 0 hasta N-1.
N = 50              # Tamaño de las listas.
c = [None] * N      # Lista de conexiones.
names = [None] * N  # Lista de nombres.

# Salida del cerrador del ciclo - entrada a la turbina de vapor.
# Establecemos la topología: de qué componente nace y a qué componente llega. Además, le asignamos un tag ("label") para identificarlo.
# Le asignamos propieades al estado. En este caso: el caudal másico m, y la lista que conforma la composición (en este caso: 100% agua -"water").
# A este estado, le agregamos una descripción y la almacenamos en names.
caudal_vapor_sobrecalentado = 2*102.3 # t/h 
c[0] = Connection(cc, 'out1', st_ext, 'in1', label='1')
c[0].set_attr(
                m=caudal_vapor_sobrecalentado, 
                fluid={'water': 1}
              )
names[0] = 'hp steam'

# Salida de la turbina de vapor (de las ruedas de alta presión) - entrada al derivador interno de la turbina.
# Este derivador es necesario para repartir el caudal: parte se dirige a la extracción de la turbina, y parte acomete a las ruedas de menor presión.
c[1] = Connection(st_ext, 'out1', sp_1, 'in1', label='2')
names[1] = 'extraction st outlet'

# Salida del derivador interno de la turbina - entrada al atemperador de media presión.
# Preliminarmente, establecemos el caudal aquí, ya que hacerlo en el vapor que va a proceso le genera un problema a la librería.
caudal_extraccion_turbina = 160 # t/h
c[2] = Connection(sp_1, 'out2', me_1, 'in2', label='3')
c[2].set_attr(m=caudal_extraccion_turbina)
names[2] = 'Steam from TV to attemp'

# Salida del derivador interno de la turbina - entrada a la válvula de control interna de la turbina.
# Esta válvula de control está en la entrada de las ruedas de media y baja presión.
c[3] = Connection(sp_1, 'out1', cond_st_cv, 'in1', label='4')
names[3] = 'cond st cv inlet'

# Salida de la válvula de control interna de la turbina - entrada a la turbina de vapor (ruedas de media y baja presión a condensación).
c[4] = Connection(cond_st_cv, 'out1', st_cond, 'in1', label='5')
names[4] = 'cond st inlet'

# Salida de la turbina de vapor a condensación - entrada al condensador.
c[5] = Connection(st_cond, 'out1', condenser, 'in1', label='6') # condenser inlet
names[5] = 'condenser inlet'

# Salida del condensador - entrada al colector de bombeo del condensador (derivador, "splitter").
# Como estamos utilizando el componente "SimpleHeatExchanger", es necesario proveer la condición de salida (saturación, y presión ó temperatura).
# Indicamos la temperatura como un valor relacionado con la temperatura ambiente.
c[6] = Connection(condenser, 'out1', sp_2, 'in1', label='7')
c[6].set_attr(x=0, T=Tamb + 18)
names[6] = 'condenser outlet'

# Salida del colector de bombeo del condensador - entrada (succión) a la bomba de extracción de condensado.
c[7] = Connection(sp_2, 'out1', cond_pump, 'in1', label='8')
names[7] = 'cond pump inlet'

# Salida del colector de bombeo del condensador - entrada (succión) a la bomba de agua de atemperación.
c[8] = Connection(sp_2, 'out2', att_pump, 'in1', label='9')
names[8] = 'att pump inlet'

# Salida de la bomba de agua de atemperación - entrada al atemperador de vapor de media presión.
c[9] = Connection(att_pump,'out1', me_1,'in1',label='10')
names[9] = 'att pump outlet'

# Salida del atemperador de vapor de media presión - entrada de vapor al proceso industrial.
# Se define su presión (absoluta) y su grado de sobrecalentamiento.
presion_vapor_proceso = 13 # bar(a)
grado_sobrecalentamiento = 10 # C
c[10] = Connection(me_1, 'out1',process_steam,'in1',label='11')
c[10].set_attr(
                Td_bp=grado_sobrecalentamiento, 
                p=presion_vapor_proceso
                )
names[10] = 'process steam'

# Salida (descarga) de la bomba de extracción de condensado - entrada a la cañería de condensado (la que acomete al tanque de mezcla).
# Suponemos que se requiere una presión de descarga de 3 bar(g).
c[11] = Connection(cond_pump,'out1', me_3, 'in1', label='12')
c[11].set_attr(p=pamb)
names[11] = 'cond pump outlet'

# Retorno de condensado del proceso industrial - entrada a la cañería de condensado (la que acomete al tanque de mezla).
retorno_condensado = 0.75 # dim # esta variable podría reposicionarse en un preámbulo, junto con los datos puestos para los estados.
#temperatura_retorno_condensado = 72.5 # C
c[12] = Connection(water_inlet_1, 'out1', me_3, 'in2', label='13')
#c[12].set_attr(T=temperatura_retorno_condensado , m=Ref(c[10], retorno_condensado, 0), fluid={'water': 1})
c[12].set_attr( m=Ref(c[10], retorno_condensado, 0), fluid={'water': 1})
names[12] = 'Condensate return from process'

# Salida de la cañería de condensado - entrada al tanque de mezcla.
#c[13] = Connection(me_2,'out1',me_3,'in1',label='14')
#names[13] = 'Condensate going to merge with water reposition'

# Provisión de agua de reposición - entrada al tanque de mezcla.
c[13] = Connection(water_inlet_2,'out1',me_3,'in3',label='14')
c[13].set_attr(T=Tamb)
names[13] = 'Water makeup'


# TBD - Entrada a bomba de alimentacion de baja preison.
c[14] = Connection(me_3,'out1',lp_pump,'in1', label='15')
names[14] = 'Water mixture feed to low pressure pump'

# TBD - Entrada al intercambiador de calor de placas.
c[15] = Connection(lp_pump,'out1',HE,'in2', label='16')
c[15].set_attr(p=2.3, T=55)
names[15] = 'Water mixture feed to heat exchanger'


# Salida del intercdambiador de calor de placas - Entrada al domo de baja presión.
# mmmmm. Yo diría que veamos los datos. 10 grados por debajo de la saturación me parece demasiado. Trataría de especificar el aumento de temperatura de la corriente. Ahí vi en la documentación que indica los TTD. Quizás podamos especificar eso.
c[16] = Connection(HE,'out2',LPDRUM,'in1',label='17')
c[16].set_attr(T=100)
names[16] = 'heated water feed to LPDRUM'

# number of states
c[17] = Connection(HE,'out1',sg_pump,'in1',label='18')
names[17] = 'Cooled water feed to HP pump'

# number of states
c[18] = Connection(sg_pump, 'out1', sp_3,'in1', label='19')
c[18].set_attr(p=88.52)
names[18] = 'pressurized water to HPEC1'

# number of states
c[19] = Connection(sp_3, 'out1', me_4, 'in2', label='20')
c[19].set_attr(m=0) 
names[19] = 'pressurized water to sg condenser'

# number of states
c[20] = Connection(sp_3, 'out2', HPEC1, 'in2', label='21')
names[20] = 'pressurized water to HPEC1'

# number of states
c[21] = Connection(HPEC1, 'out2', HPEC2, 'in2', label='22')
c[21].set_attr(T=116.1)
names[21] = 'pressurized water to HPEC2'

# number of states
c[22] = Connection(HPEC2, 'out2', me_4, 'in1', label='23')
c[22].set_attr(T=230.9)
names[22] = 'outlet of HPEC2 to merge with cold flow'

c[23] = Connection(me_4, 'out1', HE_cond, 'in1', label='24')
names[23] = 'outlet of merge to sweet water condenser'

# number of states
c[24] = Connection(HE_cond, 'out1', HPEC3, 'in2', label='25')
names[24] = 'outlet of sweet water condenser to HPEC3'

# number of states
c[25] = Connection(HPEC3, 'out2', HPDRUM, 'in1', label='26')
c[25].set_attr(T=289.9)
names[25] = 'outlet of HPEC3 to HP drum'

# number of states
c[26] = Connection(HPDRUM, 'out1', bd_2, 'in1', label='27')
names[26] = 'saturated liquid outlet of HPDRUM to Splitter'

c[27] = Connection(bd_2, 'out1', HPEV1, 'in1', label='28')
names[27] = 'saturated liquid outlet of HPDRUM to HPEV1'

c[28] = Connection(bd_2, 'out2', wst_2, 'in1', label='29')
names[28] = 'saturated liquid outlet of HPDRUM to waste'
c[28].set_attr(m=2)

# number of states
c[29] = Connection(HPEV1, 'out1', HPDRUM, 'in2', label='30')
c[29].set_attr(x=0.05)
names[29] = 'saturated steam outlet of HPEV1 to HPDRUM'

# number of states
c[30] = Connection(HPDRUM, 'out2', sp_4 , 'in1', label='31')
names[30] = 'saturated steam outlet of HPDRUM' 

# number of states
c[31] = Connection(sp_4, 'out1', HPS1, 'in2', label='32')
c[31].set_attr()
names[31] = 'saturated steam inlet to HPS1' 

# number of states
c[32] = Connection(HPS1, 'out2', me_5, 'in1', label='33')
c[32].set_attr(T=528.6)
names[32] = 'Steam outlet of HPS1 to attemp' 

# number of states
c[33] = Connection(sp_4,'out2',HE_cond,'in2', label='34')
names[33] = 'Steam derivation of HPDRUM to sweet water condenser'

# number of states
c[34] = Connection(HE_cond, 'out2', me_5, 'in2', label='35')
c[34].set_attr(x=0)
names[34] = 'Sweet water condenser outlet to attemp'

# number of states
c[35] = Connection(me_5, 'out1', HPS2, 'in2', label='36')
c[35].set_attr(T=428.8)
names[35] = 'Attemp outlet to HPS2'

# number of states
c[36] = Connection(HPS2, 'out2', cc, 'in1', label='37')
temperatura_vapor_sobrecalentado = 480 # C
c[36].set_attr(T=temperatura_vapor_sobrecalentado)
names[36] = 'Superheated steam to steam turbine'

# number of states
c[37] = Connection(LPDRUM,'out1', bd_1,'in1', label='38')
names[37] = 'Saturated liquid outlet of LPDRUM to LPEV1'

# number of states
c[38] = Connection(bd_1, 'out1', HE, 'in1', label='39')
# esta se tiene que poder poner con Ref.
names[38] = 'LPDRUM saturated liquid outlet to HE'

# number of states
c[39] = Connection(bd_1, 'out2', LPEV1, 'in1', label='40')
names[39] = 'Saturated liquid inlet to LPEV1'


# number of states
c[40] = Connection(LPEV1, 'out1', LPDRUM, 'in2', label='41')
c[40].set_attr(x=0.05)
names[40] = 'Saturated steam inlet to LPDRUM'

# number of states
c[41] = Connection(LPDRUM, 'out2', wst, 'in1', label='42')
names[41] = 'Saturated steam outlet to vent'
c[41].set_attr(m=2*0.05)



# Parte B: Lado gases de escape de turbina de gas

# Salida de turbina de gas - entrada a la segunda etapa del sobrecalentador de alta presión.
# Se indican las fracciones másicas de los gases exhaustos provenientes de la turbina de gas, así como su caudal, presión y temperatura.
c[42] = Connection(turbine_exhaust, 'out1', HPS2, 'in1', label='43')
x_gh_CO2 = 0.061 # dim
x_gh_H2O = 0.07768 # dim
x_gh_N2 = 0.7364 # dim
x_gh_O2 = 0.1126 # dim
x_gh_Ar = 1 - x_gh_CO2 - x_gh_H2O - x_gh_N2 - x_gh_O2
T_gh = 712.9 # C
G_gh = 2*481.98 # t/h
p_gh = pamb # bar(a)
c[42].set_attr(
                m=G_gh,
                T=T_gh,
                p=p_gh, 
                fluid={'O2': x_gh_O2, 'N2': x_gh_N2, 'CO2': x_gh_CO2, 'water': x_gh_H2O, 'Ar': x_gh_Ar}
                )
names[42] = 'Hot gases input to HPS2'

# Salida de la segunda etapa del sobrecalentador de alta presión - entrada a la primera etapa del sobrecalentador de alta presión.
c[43] = Connection(HPS2, 'out1', HPS1, 'in1', label='44') 
names[43] = 'Hot gases input to HPS1'

# Salida de la primera etapa del sobrecalentador - entrada al evaporador de alta presión.
c[44] = Connection(HPS1, 'out1', HPEV1, 'in2', label='45')
names[44] = 'Hot gases input to HPEV1'

# Salida del evaporador - entrada a la tercera etapa del economizador de alta presión.
c[45] = Connection(HPEV1, 'out2', HPEC3, 'in1', label='46')
names[45] = 'Hot gases input to HPEC3'

# Salida de la tercera etapa del economizador de alta presión - entrada a la segunda etapa del economizador de alta presión.
c[46] = Connection(HPEC3, 'out1', HPEC2, 'in1', label='47')
names[46] = 'Hot gases input to HPEC2'

# Salida de la segunda etapa del economizador de alta presión - entrada al evaporador de baja presión.
c[47] = Connection(HPEC2, 'out1', LPEV1 , 'in2', label='48')
names[47] = 'Hot gases input to LPEV1'

# Salida del evaporador de baja presión - entrada a la primera etapa del economizador de alta presión.
c[48] = Connection(LPEV1, 'out2', HPEC1 , 'in1', label='49')
names[48] = 'Hot gases input to HPEC1'

# Salida de la primera etapa del economizador de alta presión - entrada a la chimenea (sumidero de los gases exhaustos).
c[49] = Connection(HPEC1, 'out1', gases_outlet , 'in1', label='50')
names[49] = 'Hot gases outlet'

# ***************************

# Sección 05: Análisis exergético

power = Bus('total output power')

"Esto no entiendo cómo se relaciona con el otro bus que figura más arriba, porque aparecen los 'char' dos veces."

power.add_comps(
    {'comp': st_ext, 'char': 0.9, 'base': 'component'},
    {'comp': st_cond, 'char': 0.9, 'base': 'component'},
    {'comp': att_pump, 'char': 0.7, 'base': 'bus'},
    {'comp': cond_pump, 'char': 0.7, 'base': 'bus'},
    {'comp': sg_pump, 'char': 0.9, 'base': 'bus'},
    {'comp': process_steam, 'base': 'bus'})

heat_input_bus = Bus('heat input')
heat_input_bus.add_comps(
                        {'comp': turbine_exhaust},
                        {'comp': gases_outlet}
                        )

exergy_loss_bus = Bus('exergy loss')
exergy_loss_bus.add_comps(
                        {'comp': wst, 'base': 'bus'},
                        {'comp': condenser, 'base': 'bus'}
                        )

my_plant.add_busses(power, heat_input_bus, exergy_loss_bus)

ean = ExergyAnalysis(my_plant, E_P=[power], E_F=[heat_input_bus], E_L=[exergy_loss_bus])

ean.analyse(pamb=pamb, Tamb=Tamb)

# ***************************

# Sección 06: Resolución del sistema

# Incorporación de conexiones al objeto "Network" (la cual representa la red que conforma la planta). Una vez hecho esto, la variable "my_plant" ya contiene la red.
for j in range(0,N):
    my_plant.add_conns(c[j])

# Resolución para el modo de diseño ("design") del proceso. Impresión de resultados.
my_plant.solve(mode='design')
my_plant.print_results()

# ***************************

# Sección 07: Postprocesado

bus_results = my_plant.results['electrical power output']
df_results_for_conns = my_plant.results['Connection']

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

ean.print_results()

# ***************************

# Sección 08: Exportación de resultados

# Para exportar los resultados a un archivo determinado, se utiliza la función declara en el inicio del script.       
export(__file__, results)