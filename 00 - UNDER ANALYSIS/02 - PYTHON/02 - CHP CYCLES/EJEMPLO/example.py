    ### GENERAL INFO ###
    
    # pbarral@fi.uba.ar
    # 2025-01-27
    # tespy v0.78.post2

    ### NETWORK ###

from tespy.networks import Network

my_plant = Network()

my_plant.set_attr(
                T_unit='C',
                p_unit='bar', 
                h_unit='kJ / kg', 
                m_unit='t / h', 
                s_unit='kJ / kgK', 
                iterinfo=False
                )

    ### COMPONENTS ###

        ### DEFINITIONS ###

from tespy.components import (
    Turbine, Valve, SimpleHeatExchanger, Pump, DropletSeparator, Condenser, Splitter, Merge, Sink, Source
)

makeup = Source('make-up water')
proc_cond = Source('process condensate')
proc_steam = Sink('process steam')
bd = Sink('flashed blowdown')

condenser = Condenser('condenser')

st_ext = Turbine('extraction steam turbine')
st_cond = Turbine('condensing steam turbine')
st_splitter = Splitter('steam turbine splitter')

attemp = Merge('attemperator')
attemp_valve = Valve('attemperator valve')

ip_header = Splitter('IP header')
ip_header_valve = Valve('IP header valve')

bfw_tank = Merge('boiler feed water tank', num_in=5)
bfw_tank_splitter = Splitter('boiler feed water tank splitter')

bfwp = Pump('boiler feed water pump')
attp = Pump('attemperator pump')
mkp = Pump('makeup water pump')
mkp_valve = Valve('makeup water pump valve')
condp = Pump('process condensate pump')
condp_valve = Valve('process condensate pump valve')

cep = Pump('condensate extraction pump')
cep_valve = Valve('condensate extraction pump valve')

flash_tank = DropletSeparator('flash tank')
flash_tank_valve = Valve('flash tank valve')

boiler = SimpleHeatExchanger('boiler')
boiler_bd = SimpleHeatExchanger('boiler blowdown')
boiler_valve = Valve('boiler valve')
boiler_bd_splitter = Splitter('boiler blowdown splitter')

cwso = Source('cooling water source')
cwsi = Sink('cooling water sink')

aux_sink_01 = Sink('auxiliar sink 01')

        ### ATTRIBUTES ###

st_ext.set_attr(eta_s=0.7)
st_cond.set_attr(eta_s=0.7)
condenser.set_attr(pr1=1, pr2=1)
cep.set_attr(eta_s=0.7)
attp.set_attr(eta_s=0.7)
bfwp.set_attr(eta_s=0.7)
mkp.set_attr(eta_s=0.7)
condp.set_attr(eta_s=0.7)

    ### BUSES ###

from tespy.connections import Bus

powergen = Bus("electrical power output")
my_plant.add_busses(powergen)

powergen.add_comps(
                    {"comp": st_ext, "char": 1, "base": "component"},
                    {"comp": st_cond, "char": 1, "base": "component"},
                    {"comp": cep, "char": 1, "base": "bus"},
                    {"comp": attp, "char": 1, "base": "bus"},
                    {"comp": bfwp, "char": 1, "base": "bus"},
                    {"comp": mkp, "char": 1, "base": "bus"},
                    {"comp": condp, "char": 1, "base": "bus"},
                    )

    ### CONNECTIONS ###
            
        ### DEFINITIONS ###

from tespy.connections import (Connection, Ref)

c01 = Connection(boiler, 'out1', st_ext, 'in1', label='01 - boilert outlet/st inlet')
c02 = Connection(st_ext, 'out1', st_splitter, 'in1', label='02 - extraction st outlet')
c03 = Connection(st_splitter, 'out2', st_cond, 'in1', label='03 - condensing st  inlet')
c04 = Connection(st_cond, 'out1', condenser, 'in1', label='04 - condensing st outlet/condenser inlet')
c05 = Connection(condenser, 'out1', cep, 'in1', label='05 - condenser outlet/cep inlet')
c06 = Connection(cep, 'out1', cep_valve, 'in1', label='06 - cep outlet')
c07 = Connection(st_splitter, 'out1', attemp, 'in1', label='07 - steam attemperator inlet')
c08 = Connection(attemp, 'out1', ip_header, 'in1', label='08 - attemperator outlet/IP header inlet')
c09 = Connection(ip_header, 'out1', proc_steam, 'in1', label='09 - IP header outlet/process steam')
c10 = Connection(ip_header, 'out2', ip_header_valve, 'in1', label='10 - IP header outlet/deareator steam')
c11 = Connection(bfw_tank, 'out1', bfw_tank_splitter, 'in1', label='11 - bfw tank outlet')
c12 = Connection(bfw_tank_splitter, 'out1', attp, 'in1', label='12 - bfw tank outlet/attemperation pump inlet')
c13 = Connection(attemp_valve, 'out1', attemp, 'in2', label='13 - water attemperation inlet/attemperator valve outlet')
c14 = Connection(bfw_tank_splitter, 'out2', bfwp, 'in1', label='14 - bfw tank outlet/bfw pump inlet')
c15 = Connection(bfwp, 'out1', boiler_valve, 'in1', label='15 - bfw pump outlet')
c16 = Connection(boiler_bd_splitter, 'out1', boiler, 'in1', label='16 - bfw to steam')
c17 = Connection(boiler_bd_splitter, 'out2', boiler_bd, 'in1', label='17 - bfw to bd')
c18 = Connection(boiler_bd, 'out1', flash_tank_valve, 'in1', label='18 - boiler blowdown')
c19 = Connection(flash_tank, 'out2', bfw_tank, 'in5', label='19 - flashed bd')
c20 = Connection(flash_tank, 'out1', bd, 'in1', label='20 - bd to waste')
c21 = Connection(makeup, 'out1', mkp, 'in1', label='21 - makeup water')
c22 = Connection(mkp, 'out1', mkp_valve, 'in1', label='22 - makeup water pump outlet')
c23 = Connection(proc_cond, 'out1', condp, 'in1', label='23 - process condensate')
c24 = Connection(condp, 'out1', condp_valve, 'in1', label='24 - condp outlet')
c26 = Connection(condp_valve, 'out1', bfw_tank, 'in1', label='26 - bfwt condensate inlet')
c27 = Connection(cep_valve, 'out1', bfw_tank, 'in2', label='27 - cep valve outlet/bfwt inlet')
c28 = Connection(mkp_valve, 'out1', bfw_tank, 'in3', label='28 - bfwt makeup water inlet')
c29 = Connection(boiler_valve, 'out1', boiler_bd_splitter, 'in1', label='29 - bfw pump outlet')
c30 = Connection(attp, 'out1', attemp_valve, 'in1', label='30 - attemperation pump outlet/attemperator valve inlet')
c31 = Connection(ip_header_valve, 'out1', bfw_tank, 'in4', label='31 - laminated steam for deaeration')
c32 = Connection(flash_tank_valve, 'out1', flash_tank, 'in1', label='32 - bd to flash tank')

c98 = Connection(cwso, 'out1', condenser, 'in2', label='98 - condenser cooling water inlet')
c99 = Connection(condenser, 'out2', cwsi, 'in1', label='99 - condenser cooling water outlet')

my_plant.add_conns(c01, c02, c03, c04, c05, c06, c07, c08, c09, c10, 
                   c11, c12, c13, c14, c15, c16, c17, c18, c19, c20,
                   c21, c22, c23, c24, c26, c27, c28, c29, c30, 
                   c31, c32,
                   c98, c99)

        ### ATTRIBUTES ###

c01.set_attr(T=480, p=66.01, fluid={'water': 1})
c02.set_attr(p=13.01)
c03.set_attr(m=50)
c04.set_attr(p=0.1)
c06.set_attr(p=4.01)
c08.set_attr(Td_bp=10)
c09.set_attr(m=200)
c11.set_attr(T=105, x=0)
c15.set_attr(p=74.01)
c17.set_attr(m=Ref(c29, 0.01, 0))
c18.set_attr(p=66.01, x=0)
c21.set_attr(T=20, p=1.01)
c22.set_attr(p=4.01)
c23.set_attr(m=Ref(c09, 0.7, 0), T=70, p=1.01)
c24.set_attr(p=4.01)
c29.set_attr(p=66.01)
c30.set_attr(p=25.01)

c98.set_attr(T=20, p=4.01, fluid={'water': 1})
c99.set_attr(T=30)

    ### SOLVING AND PRINTING ###

my_plant.solve(mode='design')

results = my_plant.results['Connection']
results = results[[
    'p',
    'T',
    'h',
    's',
    'x',
    'm'
]].copy()

results.columns = ['p [bar(a)]', 't [°C]', 'h [kJ/kg]', 
                   's [kJ/kg-K]', 'x [dim]', 'm [t/h]']

from tabulate import tabulate

columns_to_format = ['p [bar(a)]', 't [°C]', 'h [kJ/kg]', 's [kJ/kg-K]', 'x [dim]', 'm [t/h]']
results[columns_to_format] = results[columns_to_format].apply(
    lambda col: col.apply(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)
)

print(tabulate(results, headers='keys', tablefmt='fancy_grid', numalign='right', stralign='center'))

    ### NOTES ###

"If 13 mass flow is to be calculated from 8 superheating degree and state 7 conditions, 13 enthalpy must be provided."

"If 13 temperature is provided, though it is a simple calculation, the problem turns into an ill-conditioned one, and tespy cannot handle it."
"Likely to be connected to the overlapping of curves in the Ts diagram for subcooled liquid, but not sure."

"When a valve (temp. control valve, for instance) is provided upstream of 13, this problem disappears, since the natural result from a valve is an enthalpy value. Upstream this valve, a temperature can be provided."

"c13.set_attr(h=400, fluid={'water': 1}) # Doesn't work if T is set. Numerically ill-conditioned."

   ### THE END ###