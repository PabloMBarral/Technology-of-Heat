def pressure_from_altitude(Z: float) -> float:
    "pressure p[kPa(a)] // altitude (above sea level) Z [m ]"
    "3 ASHRAE 2021"
    
    A = 101.325
    B = 2.25577 * 10**(-5)
    C = 5.2599
    
    p = A * (1 - B * Z)**C
    return p

def inverse_pressure_from_altitude(p: float) -> float:
    "pressure p[kPa(a)] // altitude (above sea level) Z [m ]"
    "3 ASHRAE 2021"
    
    A = 101.325
    B = 2.25577 * 10**(-5)
    C = 5.2599
    
    Z = (1 - (p / A)**(1 / C)) / B
    
    return Z

def C_to_F(t_C: float) -> float:
    t_F = (t_C + 32) * 9/5
    return t_F

def F_to_C(t_F: float) -> float:
    t_C = (t_F - 32) * 5/9
    return t_C

def C_to_K(t_C: float) -> float:
    t_K = t_C + 273.15
    return t_K

def K_to_C(t_K: float) -> float:
    t_C = t_K - 273.15
    return t_C


"kg to lb"
"lb to kg"

"Btu to kJ"
"kJ to Btu"

"m to ft"
"ft to m"

"m3 to ft3"
"ft3 to m3"

"kPa(a) to psia"
"psia to kPa(a)"


X = "IP"
X = "SI"


from CoolProp.HumidAirProp import HAPropsSI
# h = HAPropsSI('H','T',298.15,'P',101325,'R',0.5); print(h)

"""
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
Tdbvec = np.linspace(-30, 55, 200) + 273.15

# Calcular líneas de humedad relativa constante para temperaturas de bulbo seco específicas
RH_values = np.arange(0.1, 1, 0.1)
for RH in RH_values:
    W_values = [CP.HAPropsSI("W", "R", RH, "P", 101325, "T", Tdb) for Tdb in Tdbvec]
    plt.plot(Tdbvec - 273.15, W_values, color='k', lw=0.5)

# Calcular la curva de saturación
W_sat = CP.HAPropsSI("W", "R", 1, "P", 101325, "T", Tdbvec)
plt.plot(Tdbvec - 273.15, W_sat, color='k', lw=1.5)

# Calcular líneas de volumen específico de aire seco constante
Vda_values = np.arange(0.69, 0.961, 0.01)
for Vda in Vda_values:
    R = np.linspace(0, 1, 100)
    W = CP.HAPropsSI("W", "R", R, "P", 101325, "Vda", Vda)
    Tdb = CP.HAPropsSI("Tdb", "R", R, "P", 101325, "Vda", Vda)
    plt.plot(Tdb - 273.15, W, color='b', lw=1.5 if abs(Vda % 0.05) < 0.001 else 0.5)

# Calcular líneas de bulbo húmedo constante
Twb_values = np.arange(-16, 33, 2)
for Twb_C in Twb_values:
    if Twb_C != 0:
        R = np.linspace(0.0, 1, 100)
        Tdb = CP.HAPropsSI("Tdb", "R", R, "P", 101325, "Twb", Twb_C + 273.15)
        W = CP.HAPropsSI("W", "R", R, "P", 101325, "Tdb", Tdb)
        plt.plot(Tdb - 273.15, W, color='r', lw=1.5 if abs(Twb_C % 10) < 0.001 else 0.5)

# Estado específico
Tdb_C = 25  # Temperatura de bulbo seco en grados Celsius
RH = 0.5    # Humedad Relativa

# Convertir Tdb a Kelvin
Tdb = Tdb_C + 273.15

# Calcular la Humedad Específica para el estado específico
W_state = CP.HAPropsSI("W", "T", Tdb, "R", RH, "P", 101325)

# Calcular otras propiedades
Twb_state_C = CP.HAPropsSI("Twb", "T", Tdb, "R", RH, "P", 101325) - 273.15
H_state_kJ = CP.HAPropsSI("H", "T", Tdb, "R", RH, "P", 101325) / 1000
HumAbs_state = CP.HAPropsSI("Vha", "T", Tdb, "R", RH, "P", 101325)
DewPoint_state_C = CP.HAPropsSI("Tdp", "T", Tdb, "R", RH, "P", 101325) - 273.15

# Dibujar el estado específico
plt.plot(Tdb_C, W_state, 'ro')  # 'ro' significa color rojo, marcador de círculo
plt.text(Tdb_C, W_state, f'({Tdb_C}°C, {RH*100}%)', color='red', fontsize=12)

# Mostrar información adicional
info_text = (f'Twb: {Twb_state_C:.2f}°C\n'
             f'h: {H_state_kJ:.2f} kJ/kg\n'
             f'HumAbs: {HumAbs_state:.2f} kgw/kgda\n'
             f'DewPoint: {DewPoint_state_C:.2f}°C')

plt.text(-25, 0.027, info_text, color='black', fontsize=10, verticalalignment='top')

plt.xlabel(r'Temperatura de bulbo seco $T_{\rm db}$ ($^{\circ}$ C)')
plt.ylabel(r'Humedad Específica $W$ (kg/kg)')
plt.ylim(0, 0.030)
plt.xlim(-30, 55)
plt.show()
"""








"""
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1,1,figsize=(10, 8))
Tdbvec = np.linspace(-30, 55)+273.15

# Lines of constant relative humidity
for RH in np.arange(0.1, 1, 0.1):
    W = CP.HAPropsSI("W","R",RH,"P",101325,"T",Tdbvec)
    plt.plot(Tdbvec-273.15, W, color='k', lw = 0.5)

# Saturation curve
W = CP.HAPropsSI("W","R",1,"P",101325,"T",Tdbvec)
plt.plot(Tdbvec-273.15, W, color='k', lw=1.5)

# Lines of constant Vda
for Vda in np.arange(0.69, 0.961, 0.01):
    R = np.linspace(0,1)
    W = CP.HAPropsSI("W","R",R,"P",101325,"Vda",Vda)
    Tdb = CP.HAPropsSI("Tdb","R",R,"P",101325,"Vda",Vda)
    plt.plot(Tdb-273.15, W, color='b', lw=1.5 if abs(Vda % 0.05) < 0.001 else 0.5)

# Lines of constant wetbulb
for Twb_C in np.arange(-16, 33, 2):
    if Twb_C == 0:
        continue
    R = np.linspace(0.0, 1)
    print(Twb_C)
    Tdb = CP.HAPropsSI("Tdb","R",R,"P",101325,"Twb",Twb_C+273.15)
    W = CP.HAPropsSI("W","R",R,"P",101325,"Tdb",Tdb)
    plt.plot(Tdb-273.15, W, color='r', lw=1.5 if abs(Twb_C % 10) < 0.001 else 0.5)

plt.xlabel(r'Dry bulb temperature $T_{\rm db}$ ($^{\circ}$ C)')
plt.ylabel(r'Humidity Ratio $W$ (kg/kg)')
plt.ylim(0, 0.030)
plt.xlim(-30, 55)
plt.show()
"""

"""
import numpy as np
import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
Tdbvec = np.linspace(-30, 55) + 273.15

# Lines of constant relative humidity
for RH in np.arange(0.1, 1, 0.1):
    W = CP.HAPropsSI("W", "R", RH, "P", 101325, "T", Tdbvec)
    plt.plot(Tdbvec - 273.15, W, color='k', lw=0.5)
    # Etiqueta de la línea de humedad relativa
    plt.text(Tdbvec[-1] - 273.15, W[-1], f'{int(RH*100)}%', fontsize=8, verticalalignment='bottom')

# Saturation curve
W = CP.HAPropsSI("W", "R", 1, "P", 101325, "T", Tdbvec)
plt.plot(Tdbvec - 273.15, W, color='k', lw=1.5)
# Etiqueta de la curva de saturación
plt.text(Tdbvec[-1] - 273.15, W[-1], '100% RH', fontsize=8, verticalalignment='bottom')

# Lines of constant Vda
for Vda in np.arange(0.69, 0.961, 0.01):
    R = np.linspace(0, 1)
    W = CP.HAPropsSI("W", "R", R, "P", 101325, "Vda", Vda)
    Tdb = CP.HAPropsSI("Tdb", "R", R, "P", 101325, "Vda", Vda)
    plt.plot(Tdb - 273.15, W, color='b', lw=1.5 if abs(Vda % 0.05) < 0.001 else 0.5)
    # Etiqueta de la línea de volumen específico
    plt.text(Tdb[-1] - 273.15, W[-1], f'{Vda:.2f} m³/kg', fontsize=8, color='b', verticalalignment='bottom')

# Lines of constant wetbulb
for Twb_C in np.arange(-16, 33, 2):
    if Twb_C == 0:
        continue
    R = np.linspace(0.0, 1)
    Tdb = CP.HAPropsSI("Tdb", "R", R, "P", 101325, "Twb", Twb_C + 273.15)
    W = CP.HAPropsSI("W", "R", R, "P", 101325, "Tdb", Tdb)
    plt.plot(Tdb - 273.15, W, color='r', lw=1.5 if abs(Twb_C % 10) < 0.001 else 0.5)
    # Etiqueta de la línea de temperatura de bulbo húmedo
    plt.text(Tdb[-1] - 273.15, W[-1], f'{Twb_C}°C', fontsize=8, color='r', verticalalignment='bottom')

plt.xlabel(r'Dry bulb temperature $T_{\rm db}$ ($^{\circ}$C)')
plt.ylabel(r'Humidity Ratio $W$ (kg/kg)')
plt.ylim(0, 0.030)
plt.xlim(-30, 55)
plt.title('Psychrometric Chart')
plt.grid(True)
plt.show()
"""
# psychrolib
" psycrochart"
"""
from psychrochart import PsychroChart

# Load default style:
chart_default = PsychroChart.create()
# customize anything
chart_default.config.limits.range_temp_c = (15.0, 35.0)
chart_default.config.limits.range_humidity_g_kg = (5, 25)
chart_default.config.saturation.linewidth = 1
chart_default.config.constant_wet_temp.color = "darkblue"
# plot
axes = chart_default.plot()
axes.get_figure()
# or store on disk
chart_default.save("my-custom-chart.svg")
"""
# https://pint.readthedocs.io/en/stable/user/nonmult.html
# https://fluids.readthedocs.io/tutorial.html#miscellaneous-utilities
# http://www.coolprop.org/fluid_properties/HumidAir.html#humid-air-validation

# See readme.md for the sources of this calculation.


"Features"

"""
    1. Defino sistema de unidades. Convierto de imperial a SI. Esto me tiene que cambiar el front.
    2. Ingreso presión p, o ingreso altitud Z. Calculo la otra. Tengo que tener cuidado de los límites en los
    que ingreso los valores, que sean float, y que tengan sólo dos decimales, para no complicar el tema.
    3. Ingreso la temperatura de bulbo seco. Tdp
    4. Elijo si ingresar humedad relativa f (en %), bulbo húmedo Twb o bien punto de rocío Tdp
    5. Calculo: 
    HR
    v
    MU
    h
    VP
    SVP
"""
