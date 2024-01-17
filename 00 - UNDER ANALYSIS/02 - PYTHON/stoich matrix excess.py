from sympy import symbols, Eq, linear_eq_to_matrix, linsolve
import numpy as np
import os

# Definir las variables
excess, a_s = symbols('excess a_s')
a_x, b_x, c_x, d_x, e_x, f_x, g_x = symbols('a_x b_x c_x d_x e_x f_x g_x')
c, h, o, n, s = symbols('c h o n s')
y_a_co2, y_a_h2o, y_a_n2, y_a_o2, y_a_ar = symbols('y_a_co2 y_a_h2o y_a_n2 y_a_o2 y_a_ar')

# Definir el sistema de ecuaciones lineales
eq1 = Eq(c + a_x * y_a_co2 * 2, b_x)

eq2 = Eq(h + a_x * y_a_h2o * 2, 2 * c_x)

eq3 = Eq(o + a_x * (y_a_o2 * 2 + y_a_co2 * 2), 2 * b_x + c_x + 2 * e_x + 2 * g_x)

eq4 = Eq(n + a_x * y_a_n2 * 2, 2 * d_x)

eq5 = Eq(s, g_x)

eq6 = Eq(a_x * y_a_ar * 2, f_x)

eq7 = Eq(excess * a_s, a_x)

# Obtener la matriz aumentada del sistema
coef_matrix, rhs_matrix = linear_eq_to_matrix([eq1, eq2, eq3, eq4, eq5, eq6, eq7], [a_x, b_x, c_x, d_x, e_x, f_x, g_x])

# Imprimir la matriz aumentada
print("Matriz aumentada del sistema:")
print(coef_matrix.row_join(rhs_matrix))

# Resolver el sistema de ecuaciones lineales
solution = linsolve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), a_x, b_x, c_x, d_x, e_x, f_x, g_x)

# Imprimir la solución
print("\nSolución del sistema:")
print(solution)

# Crear un diccionario para almacenar los resultados
results = {}

# Resolver el sistema de ecuaciones lineales
solution = linsolve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), a_x, b_x, c_x, d_x, e_x, f_x, g_x)

# Almacenar los resultados en el diccionario
results['a_x'] = solution.args[0][0]
results['b_x'] = solution.args[0][1]
results['c_x'] = solution.args[0][2]
results['d_x'] = solution.args[0][3]
results['e_x'] = solution.args[0][4]
results['f_s'] = solution.args[0][5]
results['g_x'] = solution.args[0][6]

# Imprimir la solución en la terminal
print("\nSolución del sistema:")
print(solution)

# Obtener la ruta del directorio actual del script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa al archivo
file_path = os.path.join(script_dir, 'resultados.txt')

# Guardar los resultados en un archivo de texto
with open(file_path, 'w') as file:
    # Escribir los resultados en el archivo
    file.write("Resultados del sistema de ecuaciones lineales:\n\n")
    for variable, valor in results.items():
        file.write(f"{variable}: {valor}\n")

    # Agregar la matriz aumentada al archivo
    file.write("\nMatriz aumentada del sistema:\n")
    matrix_str = np.array_str(np.concatenate((coef_matrix, rhs_matrix), axis=1), max_line_width=np.inf)
    file.write(matrix_str)

print(f"Los resultados se han guardado en: {file_path}")