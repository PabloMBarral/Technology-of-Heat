# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 08:15:16 2021

@author: pmbarral
"""
import fluids as fl
import math as math
import numpy as np
from pint import UnitRegistry

# Generamos un objeto "Registro de unidades"
ureg=UnitRegistry()
# %% 
# Obtenemos la rugosidad absoluta del material. A las salidas de funciones
# debemos adicionar la unidad. Ante la duda, estan en SI.
material = fl.nearest_material_roughness('steel', clean=True)
epsilon = fl.material_roughness(material) * ureg.m

# Indicamos el caudal volumetrico por la caneria.
Q = 200 * ureg.m**3 / ureg.hr

# Indicamosla densidad del fluido incompresible que circula.
# No cambia su densidad ante cambios de presion. Si es un gas, esto es valido
# solo si los cambios de presion son pequenos.
rho = 1000 * ureg.kg / ureg.m**3

# Indicamos la viscosidad dinamica del fluido incompresible que circula.
mu = 1E-4 * ureg.Pa * ureg.s

# Numpy array que contiene los diametros internos de los distintos tramos 
# de la caneria.
D = np.array([150, 100, 150]) * ureg.mm

# Idem con las longitudes
L = np.array([20, 5, 15]) * ureg.m

# Inicializamos los arrays para mejorar la performance del codigo.
V = np.zeros(len(D)); Re = V; eD = V; fd = V

# Array con la velocidad por tramo de caneria.
V = Q / (math.pi / 4 * D**2)

# Array con el reynolds por tramo (como es salida de funcion, le agrego
# la unidad)
Re = fl.Reynolds(V=V, D=D, rho=rho, mu=mu) * ureg.dimensionless

# Rugosidad relativa de los distintos tramos de caneria
eD = epsilon/D

# Factor de friccion de Darcy para cada tramo.
for j in range(len(fd)):
    fd[j] = fl.friction_factor(Re[j], eD=eD[j]) * ureg.dimensionless
# %% 
# En cada paso sumamos perdidas de carga. Debemos unificar a una base, si los
# diametros de los tramos varian.

# Debido a la friccion.
K = fl.K_from_f(fd=fd[0], L=L[0], D=D[0])

# Debido a la entrada biselada.
K += fl.entrance_beveled(Di=D[0], l=10*ureg.mm, angle=30*ureg.degrees)

# Debido a un codo miter de 30 grados.
K += fl.bend_miter(angle=30*ureg.degrees)

# Debido a una contraccion aguda.
K += fl.contraction_sharp(Di1=D[0], Di2=D[1])

# Debido a la friccion para el tramo de otro diametro. Debemos cambiar la base.
# Esto es porque al final usamos una sola velocidad.
K += fl.change_K_basis(fl.K_from_f(fd=fd[1], L=L[1], D=D[1]), D1=D[1], D2=D[0])

# Debido a un codo miter de 30 gradis y a un codo redondeado de 45 grados.
K += fl.change_K_basis(K1=fl.bend_miter(angle=30*ureg.degrees), D1=D[1], D2=D[0])
K += fl.change_K_basis(K1=fl.bend_rounded(Di=D[1], angle=45*ureg.degrees, fd=fd[1]),\
                       D1=D[1], D2=D[0])

# Debido a la friccion y debido a un difusor agudo.
K += fl.change_K_basis(fl.K_from_f(fd=fd[2], L=L[2], D=D[2]), D1=D[2], D2=D[0])
K += fl.change_K_basis(fl.diffuser_sharp(Di1=D[1], Di2=D[2]), D1=D[2], D2=D[0])
# %% 
# Obtenemos la caida de presion a partir del K
dP=fl.dP_from_K(K, rho=rho, V=V[0])
dP.ito(ureg.bar)
print(dP)