from sympy import symbols, Eq, linear_eq_to_matrix, linsolve
import numpy as np
import os

# Definir las variables
a_s, b_s, c_s, d_s, e_s, f_s, g_s = symbols('a_s b_s c_s d_s e_s f_s g_s')
c, h, o, n, s = symbols('c h o n s')
y_a_co2, y_a_h2o, y_a_n2, y_a_o2, y_a_ar = symbols('y_a_co2 y_a_h2o y_a_n2 y_a_o2 y_a_ar')

# Definir el sistema de ecuaciones lineales
eq1 = Eq(c + a_s * y_a_co2 * 2, b_s)

eq2 = Eq(h + a_s * y_a_h2o * 2, 2 * c_s)

eq3 = Eq(o + a_s * (y_a_o2 * 2 + y_a_co2 * 2), 2 * b_s + c_s + 2 * g_s)

eq4 = Eq(n + a_s * y_a_n2 * 2, 2 * d_s)

eq5 = Eq(s, g_s)

eq6 = Eq(a_s * y_a_ar * 2, f_s)

eq7 = Eq(0, e_s)

# Obtener la matriz aumentada del sistema
coef_matrix, rhs_matrix = linear_eq_to_matrix([eq1, eq2, eq3, eq4, eq5, eq6, eq7], [a_s, b_s, c_s, d_s, e_s, f_s, g_s])

# Imprimir la matriz aumentada
print("Matriz aumentada del sistema:")
print(coef_matrix.row_join(rhs_matrix))

# Resolver el sistema de ecuaciones lineales
solution = linsolve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), a_s, b_s, c_s, d_s, e_s, f_s, g_s)

# Imprimir la solución
print("\nSolución del sistema:")
print(solution)

# Crear un diccionario para almacenar los resultados
results = {}

# Resolver el sistema de ecuaciones lineales
solution = linsolve((eq1, eq2, eq3, eq4, eq5, eq6, eq7), a_s, b_s, c_s, d_s, e_s, f_s, g_s)

# Almacenar los resultados en el diccionario
results['a_s'] = solution.args[0][0]
results['b_s'] = solution.args[0][1]
results['c_s'] = solution.args[0][2]
results['d_s'] = solution.args[0][3]
results['e_s'] = solution.args[0][4]
results['f_s'] = solution.args[0][5]
results['g_s'] = solution.args[0][6]

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