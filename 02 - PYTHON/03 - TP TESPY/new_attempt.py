from tespy.networks import Network
from tespy.components import (
    CycleCloser, Turbine, Pump, Valve, Source, Sink, Splitter,
    Merge, SimpleHeatExchanger, HeatExchanger, Drum,
)
#from tespy.tools import Bus
from tespy.connections import Connection, Ref, Bus

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

N = 50
#c = [None] * N
names = [''] * N

# caudal_vapor_sobrecalentado = 2*102.3 # t/h
c_00 = Connection(HPS2, 'out2', st_ext, 'in1', label='1')
c_00.set_attr(
                #m=caudal_vapor_sobrecalentado,
                fluid={'water': 1}, T=480, p0=88.5
              )
names[0] = 'hp steam'


c_01 = Connection(st_ext, 'out1', sp_1, 'in1', label='2')
names[1] = 'extraction st outlet'



caudal_extraccion_turbina = 160 # t/h
c_02 = Connection(sp_1, 'out2', me_1, 'in2', label='3')
c_02.set_attr(m=caudal_extraccion_turbina)
names[2] = 'Steam from TV to attemp'



c_03 = Connection(sp_1, 'out1', cond_st_cv, 'in1', label='4')
names[3] = 'cond st cv inlet'



c_04 = Connection(cond_st_cv, 'out1', st_cond, 'in1', label='5')
names[4] = 'cond st inlet'



c_05 = Connection(st_cond, 'out1', condenser, 'in1', label='6')
names[5] = 'condenser inlet'



c_06 = Connection(condenser, 'out1', sp_2, 'in1', label='7')
c_06.set_attr(x=0, T=Tamb + 18)
names[6] = 'condenser outlet'



c_07 = Connection(sp_2, 'out1', cond_pump, 'in1', label='8')
names[7] = 'cond pump inlet'


c_08 = Connection(sp_2, 'out2', att_pump, 'in1', label='9')
names[8] = 'att pump inlet'


c_09 = Connection(att_pump,'out1', me_1,'in1',label='10')
names[9] = 'att pump outlet'



presion_vapor_proceso = 13 # bar(a)
grado_sobrecalentamiento = 10 # C
c_10 = Connection(me_1, 'out1',process_steam,'in1',label='11')
c_10.set_attr(
                Td_bp=grado_sobrecalentamiento,
                p=presion_vapor_proceso
                )
names[10] = 'process steam'



c_11 = Connection(cond_pump,'out1', me_3, 'in1', label='12')
c_11.set_attr(p=pamb)
names[11] = 'cond pump outlet'



retorno_condensado = 0.75 # dim
c_12 = Connection(water_inlet_1, 'out1', me_3, 'in2', label='13')
c_12.set_attr( m=Ref(c_10, retorno_condensado, 0), fluid={'water': 1}, x=0)
names[12] = 'Condensate return from process'



c_13 = Connection(water_inlet_2,'out1',me_3,'in3',label='14')
c_13.set_attr(T=Tamb, fluid={"water": 1})
names[13] = 'Water makeup'



c_14 = Connection(me_3,'out1', lp_pump,'in1', label='15')
names[14] = 'Water mixture feed to low pressure pump'



c_15 = Connection(lp_pump,'out1', HE,'in2', label='16')
c_15.set_attr(p=2.3, T=55)
names[15] = 'Water mixture feed to heat exchanger'



c_16 = Connection(HE,'out2', LPDRUM,'in1',label='17')
c_16.set_attr(T=100, p0=2.3)  # here p0 is required apparently
names[16] = 'heated water feed to LPDRUM'



c_17 = Connection(HE,'out1', sg_pump,'in1', label='18')
names[17] = 'Cooled water feed to HP pump'



c_18 = Connection(sg_pump, 'out1', sp_3,'in1', label='19')
c_18.set_attr(p=88.52)
names[18] = 'pressurized water to HPEC1'

c_19 = Connection(sp_3, 'out1', me_4, 'in2', label='20')
c_19.set_attr(m=0)
names[19] = 'pressurized water to sg condenser'

c_20 = Connection(sp_3, 'out2', HPEC1, 'in2', label='21')  # in2
names[20] = 'pressurized water to HPEC1'

c_21 = Connection(HPEC1, 'out2', HPEC2, 'in2', label='22')  # in2
c_21.set_attr(T=116.1, p0=88.52)  # starting value necessary apparently
names[21] = 'pressurized water to HPEC2'

c_22 = Connection(HPEC2, 'out2', me_4, 'in1', label='23')
c_22.set_attr(T=230.9, p0=88.52)  # same here
names[22] = 'outlet of HPEC2 to merge with cold flow'

c_23 = Connection(me_4, 'out1', HE_cond, 'in2', label='24')  # this should be in2
# c_23.set_attr(p0=88.52)  # this cannot be set here due to connection with sp_3
names[23] = 'outlet of merge to sweet water condenser'

c_24 = Connection(HE_cond, 'out2', HPEC3, 'in2', label='25')  # in2
c_24.set_attr()  # temperature for initial solution
names[24] = 'outlet of sweet water condenser to HPEC3'

c_25 = Connection(HPEC3, 'out2', HPDRUM, 'in1', label='26')
c_25.set_attr(T=289.9, p0=90)
names[25] = 'outlet of HPEC3 to HP drum'

c_26 = Connection(HPDRUM, 'out1', bd_2, 'in1', label='27')
names[26] = 'saturated liquid outlet of HPDRUM to Splitter'

c_27 = Connection(bd_2, 'out1', HPEV1, 'in2', label='28')  # in2
names[27] = 'saturated liquid outlet of HPDRUM to HPEV1'

c_28 = Connection(bd_2, 'out2', wst_2, 'in1', label='29')
names[28] = 'saturated liquid outlet of HPDRUM to waste'
c_28.set_attr(m=2)

c_29 = Connection(HPEV1, 'out2', HPDRUM, 'in2', label='30')
c_29.set_attr(x=0.05)
names[29] = 'saturated steam outlet of HPEV1 to HPDRUM'

c_30 = Connection(HPDRUM, 'out2', sp_4 , 'in1', label='31')
names[30] = 'saturated steam outlet of HPDRUM'

c_31 = Connection(sp_4, 'out1', HPS1, 'in2', label='32')  #  in2
names[31] = 'saturated steam inlet to HPS1'

c_32 = Connection(HPS1, 'out2', me_5, 'in1', label='33')
c_32.set_attr(T=528.6)
names[32] = 'Steam outlet of HPS1 to attemp'

c_33 = Connection(sp_4, 'out2', HE_cond, 'in1', label='34')
names[33] = 'Steam derivation of HPDRUM to sweet water condenser'

c_34 = Connection(HE_cond, 'out1', me_5, 'in2', label='35')
c_34.set_attr(x=0)
names[34] = 'Sweet water condenser outlet to attemp'

c_35 = Connection(me_5, 'out1', HPS2, 'in2', label='36')  # in 2!
c_35.set_attr(T=428.8)
names[35] = 'Attemp outlet to HPS2'

# c_36 = Connection(HPS2, 'out1', cc, 'in1', label='37')
# temperatura_vapor_sobrecalentado = 480 # C
# c_36.set_attr(T=temperatura_vapor_sobrecalentado)
# names[36] = 'Superheated steam to steam turbine'
# not actually required because you have make up water, that means no cc required

c_37 = Connection(LPDRUM,'out1', bd_1,'in1', label='38')
names[37] = 'Saturated liquid outlet of LPDRUM to LPEV1'

c_38 = Connection(bd_1, 'out1', HE, 'in1', label='39')
names[38] = 'LPDRUM saturated liquid outlet to HE'

c_39 = Connection(bd_1, 'out2', LPEV1, 'in2', label='40')
names[39] = 'Saturated liquid inlet to LPEV1'

c_40 = Connection(LPEV1, 'out2', LPDRUM, 'in2', label='41')
c_40.set_attr(x=0.05)
names[40] = 'Saturated steam inlet to LPDRUM'  # this is not actually saturated

c_41 = Connection(LPDRUM, 'out2', wst, 'in1', label='42')
names[41] = 'Saturated steam outlet to vent'
c_41.set_attr(m=2*0.05)

c_42 = Connection(turbine_exhaust, 'out1', HPS2, 'in1', label='43')
x_gh_CO2 = 0.061 # dim
x_gh_H2O = 0.07768 # dim
x_gh_N2 = 0.7364 # dim
x_gh_O2 = 0.1126 # dim
x_gh_Ar = 1 - x_gh_CO2 - x_gh_H2O - x_gh_N2 - x_gh_O2
T_gh = 712.9 # C
G_gh = 3*481.98 # t/h
p_gh = pamb # bar(a)
c_42.set_attr(
                m=G_gh,
                T=T_gh,
                p=p_gh,
                fluid={'O2': x_gh_O2, 'N2': x_gh_N2, 'CO2': x_gh_CO2, 'water': x_gh_H2O, 'Ar': x_gh_Ar}
                )
names[42] = 'Hot gases input to HPS2'

c_43 = Connection(HPS2, 'out1', HPS1, 'in1', label='44')
names[43] = 'Hot gases input to HPS1'

c_44 = Connection(HPS1, 'out1', HPEV1, 'in1', label='45')
names[44] = 'Hot gases input to HPEV1'

c_45 = Connection(HPEV1, 'out1', HPEC3, 'in1', label='46')
names[45] = 'Hot gases input to HPEC3'

c_46 = Connection(HPEC3, 'out1', HPEC2, 'in1', label='47')
names[46] = 'Hot gases input to HPEC2'

c_47 = Connection(HPEC2, 'out1', LPEV1 , 'in1', label='48')
names[47] = 'Hot gases input to LPEV1'

c_48 = Connection(LPEV1, 'out1', HPEC1 , 'in1', label='49')
names[48] = 'Hot gases input to HPEC1'

c_49 = Connection(HPEC1, 'out1', gases_outlet , 'in1', label='50')
names[49] = 'Hot gases outlet'

nw.add_conns(c_00)
nw.add_conns(c_01)
nw.add_conns(c_02)
nw.add_conns(c_03)
nw.add_conns(c_04)
nw.add_conns(c_05)
nw.add_conns(c_06)
nw.add_conns(c_07)
nw.add_conns(c_08)
nw.add_conns(c_09)
nw.add_conns(c_10)
nw.add_conns(c_11)
nw.add_conns(c_12)
nw.add_conns(c_13)
nw.add_conns(c_14)
nw.add_conns(c_15)
nw.add_conns(c_16)
nw.add_conns(c_17)
nw.add_conns(c_18)
nw.add_conns(c_19)
nw.add_conns(c_20)
nw.add_conns(c_21)
nw.add_conns(c_22)
nw.add_conns(c_23)
nw.add_conns(c_24)
nw.add_conns(c_25)
nw.add_conns(c_26)
nw.add_conns(c_27)
nw.add_conns(c_28)
nw.add_conns(c_29)
nw.add_conns(c_30)
nw.add_conns(c_31)
nw.add_conns(c_32)
nw.add_conns(c_33)
nw.add_conns(c_34)
nw.add_conns(c_35)
#nw.add_conns(c_36)
nw.add_conns(c_37)
nw.add_conns(c_38)
nw.add_conns(c_39)
nw.add_conns(c_40)
nw.add_conns(c_41)
nw.add_conns(c_42)
nw.add_conns(c_43)
nw.add_conns(c_44)
nw.add_conns(c_45)
nw.add_conns(c_46)
nw.add_conns(c_47)
nw.add_conns(c_48)
nw.add_conns(c_49)




nw.solve(mode='design')
nw.print_results()