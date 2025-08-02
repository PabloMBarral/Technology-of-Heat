from scipy.optimize import fsolve
from ht import LMTD


t_h_i = 900
t_c_i = 100
G_h = 400
G_c = 400
c_p_h = 1
c_p_c = 1.5
U = 100
A = 1.2



# Equation system definition

def sistema_ecuaciones(variables):
    Q, t_h_o, t_c_o = variables
    dTlm = LMTD(Tci=t_c_i, Tco=t_c_o, Thi=t_h_i, Tho=t_h_o)
    eq1 = Q - U * A * dTlm
    eq2 = Q - G_c * c_p_c * (t_c_o - t_c_i)
    eq3 = Q - G_h * c_p_h * (t_h_i - t_h_o)
    return [eq1, eq2, eq3]

# Guess the values
Q0 = 100000
t_h_o0 = 800
t_c_o0 = 300

guess = [Q0, t_h_o0, t_c_o0]

# Resolver el sistema de ecuaciones no lineales
solution = fsolve(sistema_ecuaciones, guess)

# Imprimir la solución
print("Solution of the non-linear equation system:")
print("Q =", solution[0])
print("t_h_o =", solution[1])
print("t_c_o =", solution[2])
