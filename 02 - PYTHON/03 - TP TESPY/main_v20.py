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



from tespy.networks import Network

from tespy.components import (CycleCloser, Turbine, Source, Sink, Splitter, Valve, SimpleHeatExchanger, Pump,Merge,HeatExchanger, Drum)

from tespy.connections import Bus

from tespy.tools import ExergyAnalysis

powergen=Bus("electrical power output")




my_plant = Network()
my_plant.set_attr(T_unit='C',p_unit='bar', h_unit='kJ / kg', m_unit='t / h', s_unit='kJ / kgK', iterinfo=False)

my_plant.add_busses(powergen)

# Components

cc=CycleCloser('cycle closer HPDRUM to ST')
cc_1=CycleCloser('cycle closer LPDRUM to HE')

steam_inlet = Source('hp steam')
water_inlet_1= Source('Process condensate return')
water_inlet_2= Source('Water reposition')
water_inlet_3=Source('Water from boiler to HE')
turbine_exhaust=Source('Hot gases source')

st_ext = Turbine('extraction st',eta_s=0.9)
st_cond = Turbine('cond st', eta_s=0.9)
att_pump = Pump('att_pump', eta_s=0.7)
cond_pump = Pump('cond_pump', eta_s=0.7)
sg_pump = Pump('steam generator pump', eta_s=0.9)
HE_aux=SimpleHeatExchanger('HE aux',pr=1)
HE=HeatExchanger('heat exchanger',pr1=0.9,pr2=0.9)
HPEC1=HeatExchanger('HPEC1', pr1=1,pr2=1)
HPEC2=HeatExchanger('HPEC2',pr1=1)
HPEC3=HeatExchanger('HPEC3',pr1=1,pr2=1)
HPEV1=SimpleHeatExchanger('HPEV1')
HPEV1_gases=SimpleHeatExchanger('HPEV1_gases',Q=-3850000,pr=1)
HPS1=HeatExchanger('HPS1',Q=-10937000,pr1=1)
HPS2=HeatExchanger('HPS2',pr1=1,pr2=1)
LPEV1=SimpleHeatExchanger('LPEV1')
LPEV1_gases=SimpleHeatExchanger('LPEV1_gases',Q=-5550000,pr=1)

HPDRUM=Drum('HP Drum')
LPDRUM=Drum('LP Drum')

sp_1 = Splitter('st inner splitter')
sp_2 = Splitter('condensate header')
sp_3=Splitter('HPEC1 splitter')
sp_4=Splitter('HPDRUM outlet')
bd=Splitter('LPDRUM splitteer to waste')
me_1=Merge('Attemper')
me_2=Merge('St condensate & process condensate return')
me_3=Merge('Water from reposition & condensate mixture')
me_4=Merge('merge at the inlet of sweet water condenser in SG')
me_5=Merge('attemp HPS2')
cond_st_cv = Valve('cond st cv', pr=0.85)



condenser = SimpleHeatExchanger('condenser')
HE_cond = HeatExchanger('sweet water condenser',Q=16672000,pr1=1,pr2=1)

steam_outlet = Sink('Sumidero de prueba')
steam_outlet_2 = Sink('Sumidero de prueba 2')
steam_outlet_3 = Sink('Sumidero de prueba 3')
wst=Sink('LPDRUM saturated liquid waste')
process_steam = Sink('process IP steam')
gases_outlet = Sink('hot gases outlet')

powergen.add_comps(
    {"comp": st_ext, "char": 0.97, "base": "component"},{"comp": st_cond, "char": 0.97, "base": "component"},
    {"comp": att_pump, "char": 0.97, "base": "bus"},{"comp": cond_pump, "char": 0.97, "base": "bus"},{"comp": sg_pump, "char": 0.97, "base": "bus"},
)

# Connections

from tespy.connections import (Connection, Ref)

N = 49  # number of states

c = [None] * N
names = [None] * N

c[0] = Connection(cc, 'out1', st_ext, 'in1', label='1') # hrsg outlet
c[0].set_attr( m=180, fluid={'water': 1})
names[0] = 'hp steam'

c[1] = Connection(st_ext, 'out1', sp_1, 'in1', label='2') # st inner splitter
c[1].set_attr(p=13)
names[1] = 'extraction st outlet'

c[2] = Connection(sp_1, 'out2', me_1, 'in2', label='3') # process steam
c[2].set_attr(m=130)
names[2] = 'Steam from TV to attemp'

c[3] = Connection(sp_1, 'out1', cond_st_cv, 'in1', label='4') # cond st valve inlet
names[3] = 'cond st cv inlet'

c[4] = Connection(cond_st_cv, 'out1', st_cond, 'in1', label='5') # cond st inlet
#c[4].set_attr(p=11)
names[4] = 'cond st inlet'

c[5] = Connection(st_cond, 'out1', condenser, 'in1', label='6') # condenser inlet
c[5].set_attr(p=0.08)
names[5] = 'condenser inlet'

c[6] = Connection(condenser, 'out1', sp_2, 'in1', label='7') # condenser header
c[6].set_attr(x=0, p=0.08)
names[6] = 'condenser outlet'

c[7] = Connection(sp_2, 'out1', cond_pump, 'in1', label='8')
names[7] = 'cond pump inlet'

c[8] = Connection(sp_2, 'out2', att_pump, 'in1', label='9')  #El caudal m=10 lo voy a sacar cuando defina x=1 para vapor a proceso
#c[8].set_attr(m=10)
names[8] = 'att pump inlet'

c[9]=Connection(att_pump,'out1',me_1,'in1',label='10')
c[9].set_attr()
names[9]='att pump outlet'

c[10]=Connection(me_1, 'out1',process_steam,'in1',label='11')
c[10].set_attr(x=1)
names[10]='process steam'

c[11]=Connection(cond_pump,'out1', me_2, 'in1', label='12')
c[11].set_attr(p=2)
names[11]='cond pump outlet'

c[12]=Connection(water_inlet_1, 'out1', me_2, 'in2', label='13')
c[12].set_attr(T=70 , m=127, fluid={'water': 1})
names[12]='Condensate return from process'

c[13]=Connection(me_2,'out1',me_3,'in1',label='14')
c[13].set_attr()
names[13]='Condensate going to merge with water reposition'

c[14]=Connection(water_inlet_2,'out1',me_3,'in2',label='15')
c[14].set_attr(T=14,m=40)
names[14]='Water reposition'

c[15]=Connection(me_3,'out1',HE,'in2',label='16')
c[15].set_attr()
names[15]='Water mixture feed to heat exchanger'

c[16]=Connection(HE,'out2',LPDRUM,'in1',label='17')
c[16].set_attr(Td_bp=-10)
names[16]='heated water feed to LPDRUM'

#c[17]=Connection(cc_1,'out1',HE,'in1',label='18')
#c[17].set_attr(fluid={'water': 1},m=180)
#names[17]='Saturated steam from LPDRUM to HE'

c[17]=Connection(HE,'out1',sg_pump,'in1',label='18')
c[17].set_attr()
names[17]='Cooled water feed to HP pump'

'Se viene la caldera papa'

c[18]=Connection(sg_pump, 'out1', sp_3,'in1', label='19')
c[18].set_attr(p=66)
names[18]='pressurized water to HPEC1'

c[19]=Connection(sp_3, 'out1', me_4, 'in2', label='20')
c[19].set_attr(m=90) 
names[19]='pressurized water to sg condenser'

c[20]=Connection(sp_3, 'out2', HPEC1, 'in2', label='21')
c[20].set_attr()
names[20]='pressurized water to HPEC1'

c[21]=Connection(HPEC1, 'out2', HPEC2, 'in2', label='22')
c[21].set_attr(Td_bp=-139.54)
names[21]='pressurized water to HPEC2'

c[22]=Connection(HPEC2, 'out2', me_4, 'in1', label='23')
c[22].set_attr(Td_bp=-76)
names[22]='outlet of HPEC2 to merge with cold flow'

c[23]=Connection(me_4, 'out1', HE_cond, 'in1', label='24')
c[23].set_attr()
names[23]='outlet of merge to sweet water condenser'

c[24]=Connection(HE_cond, 'out1', HPEC3, 'in2', label='25')
c[24].set_attr()
names[24]='outlet of sweet water condenser to HPEC3'

c[25]=Connection(HPEC3, 'out2', HPDRUM, 'in1', label='26')
c[25].set_attr(Td_bp=-50)
names[25]='outlet of HPEC3 to HP drum'

c[26]=Connection(HPDRUM, 'out1', HPEV1, 'in1', label='27')
c[26].set_attr()
names[26]='saturated liquid outlet of HPDRUM to HPEV1'

c[27]=Connection(HPEV1, 'out1', HPDRUM, 'in2', label='28')
c[27].set_attr(x=0.05)
names[27]='saturated steam outlet of HPEV1 to HPDRUM'

c[28]=Connection(HPDRUM, 'out2', sp_4 , 'in1', label='29')
c[28].set_attr()
names[28]='saturated steam outlet of HPDRUM' 

"Salida del domo de alta"

c[29]=Connection(sp_4, 'out1', HPS1, 'in2', label='30')
c[29].set_attr(m=150)
names[29]='saturated steam inlet to HPS1' 

c[30]=Connection(HPS1, 'out2', me_5, 'in1', label='31')
c[30].set_attr()
names[30]='Steam outlet of HPS1 to attemp' 

c[31]=Connection(sp_4,'out2',HE_cond,'in2', label='32')
c[31].set_attr()
names[31]='Steam derivation of HPDRUM to sweet water condenser'

c[32]=Connection(HE_cond, 'out2', me_5, 'in2', label='33')
c[32].set_attr()
names[32]='Sweet water condenser outlet to attemp'

c[33]=Connection(me_5, 'out1', HPS2, 'in2', label='34')
c[33].set_attr()
names[33]='Attemp outlet to HPS2'

c[34]=Connection(HPS2, 'out2', cc, 'in1', label='35')
c[34].set_attr(T=480)
names[34]='Superheated steam to steam turbine'



'vamos a probar cerrar con cc la salida de vapor con la entrada a la TV'

'Funciono'

'Vamos a incorporar el domo de baja presion'


c[35]=Connection(LPDRUM,'out1', bd,'in1', label='36')
c[35].set_attr()
names[35]='Saturated liquid outlet of LPDRUM to LPEV1'

c[36]=Connection(bd, 'out1', wst, 'in1', label='37')
c[36].set_attr(m=28.068)
names[36]='LPDRUM waste'

c[37]=Connection(bd, 'out2', LPEV1, 'in1', label='38')
c[37].set_attr()
names[37]='Saturated liquid inlet to LPEV1'

c[38]=Connection(LPEV1, 'out1', LPDRUM, 'in2', label='39')
c[38].set_attr(x=0.05)
names[38]='Saturated steam inlet to LPDRUM'

c[39]=Connection(LPDRUM, 'out2', HE_aux, 'in1', label='40')
c[39].set_attr()
names[39]='Saturated steam outlet of LPDRUM to HE aux'

c[40]=Connection(HE_aux, 'out1', HE, 'in1', label='41')
c[40].set_attr(x=0)
names[40]='Saturated steam outlet of HE aux to HE'

'Quedo incorparada la salida del domo de baja a HE'

'Vamos a incorporar el lado gases'

c[41] = Connection(turbine_exhaust, 'out1', HPS2, 'in1', label='42') 
c[41].set_attr( m=936,T=570,p=0.3, fluid={'Air': 1})
names[41] = 'Hot gases input to HPS2'

c[42] = Connection(HPS2, 'out1',HPS1, 'in1', label='43') 
c[42].set_attr()
names[42] = 'Hot gases input to HPS1'

c[43]=Connection(HPS1, 'out1', HPEV1_gases, 'in1', label='44')
c[43].set_attr()
names[43] = 'Hot gases input to HPEV1'

c[44]=Connection(HPEV1_gases, 'out1', HPEC3, 'in1', label='45')
c[44].set_attr()
names[44] = 'Hot gases input to HPEC3'

c[45]=Connection(HPEC3, 'out1', HPEC2, 'in1', label='46')
c[45].set_attr()
names[45] = 'Hot gases input to HPEC2'

c[46]=Connection(HPEC2, 'out1', LPEV1_gases , 'in1', label='47')
c[46].set_attr()
names[46] = 'Hot gases input to LPEV1'

c[47]=Connection(LPEV1_gases, 'out1', HPEC1 , 'in1', label='48')
c[47].set_attr()
names[47] = 'Hot gases input to HPEC1'

c[48]=Connection(HPEC1, 'out1', gases_outlet , 'in1', label='49')
c[48].set_attr()
names[48] = 'Hot gases outlet'

'Analisis exergetico'

pamb = 1.013
Tamb = 25

power = Bus('total output power')
power.add_comps(
    {'comp': st_ext, 'char': 0.9, 'base': 'component'},
    {'comp': st_cond, 'char': 0.9, 'base': 'component'},
    {'comp': att_pump, 'char': 0.7, 'base': 'bus'},
    {'comp': cond_pump, 'char': 0.7, 'base': 'bus'},
    {'comp': sg_pump, 'char': 0.9, 'base': 'bus'},
    {'comp': process_steam,'base': 'bus'})


heat_input_bus = Bus('heat input')
heat_input_bus.add_comps({'comp':turbine_exhaust},{'comp':gases_outlet})


exergy_loss_bus = Bus('exergy loss')
exergy_loss_bus.add_comps( {'comp': wst,'base': 'bus'},{'comp': condenser,'base': 'bus'} )

my_plant.add_busses(power, heat_input_bus, exergy_loss_bus)

ean = ExergyAnalysis(my_plant, E_P=[power], E_F=[heat_input_bus], E_L=[exergy_loss_bus])

ean.analyse(pamb=pamb, Tamb=Tamb)





for j in range(0,N):
    if c[j] is not None:
        my_plant.add_conns(c[j])

my_plant.solve(mode='design')
my_plant.print_results()
bus_results = my_plant.results['electrical power output']
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


start_index_for_gases = 41
results_gases = results[start_index_for_gases:]
results_gases = results_gases[['denomination',
                                'p','p_unit',
                                'T','T_unit',
                                'h','h_unit',
                                's','s_unit',
                                'm','m_unit']]
results = results[0:start_index_for_gases]



results = results.drop(results.index[0])
results = results.round(3)

ean.print_results()

# Exportation:
        
export(__file__, results)


