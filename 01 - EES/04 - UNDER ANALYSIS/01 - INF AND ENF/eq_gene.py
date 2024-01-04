import os
import pandas as pd

def index_search(df, tag_value):
    index = df[df['tag'] == tag_value].index[0]
    return int(index)  # Convertir a entero de Python

def tuples(df, tuple_list):
    result_indices = []

    for tuple_vals in tuple_list:
        indices = [index_search(df, tag_value) for tag_value in tuple_vals]
        result_indices.extend(indices)

    return result_indices

def room_list(__file__):
    script_path = os.path.dirname(os.path.abspath(__file__))

    room_list_filename = 'room_list.xlsx'

    room_list_path = os.path.join(script_path, room_list_filename)

    df = pd.read_excel(room_list_path, header=None, engine='openpyxl', names=['tag', 'denom', 'p_design'])

    df = df.drop('p_design', axis=1)
    return df

def string_gen(df, tuple_list):
    result = []

    for tupla in tuple_list:
        in_point, fin_point = tupla
        tuple_indices = tuples(df, [(in_point,), (fin_point,)])  # Llamada a la función tuples con las tuplas de un solo elemento
        in_point_index = tuple_indices[0]
        fin_point_index = tuple_indices[1]

        resultado = f"{{{in_point} to {fin_point}}}\n"
        resultado += f"        Q[{in_point_index}; {fin_point_index}] = area('P20m') * C_d * sqrt(2 * (p[{in_point_index}] - p[{fin_point_index}]) / rho) * convert(m^3/s;m^3/h)\n"
        resultado += f"        {{Q_grid[{in_point_index}; {fin_point_index}] = 0 [m^3/h]}}\n"

        result.append(resultado)

    return result

df = room_list(__file__)

env_line = pd.DataFrame({'tag': ['2-00'], 'denom': ['EXTERIOR']})
df = pd.concat([env_line, df], ignore_index=True)

inf_list = [('2-14-1', '2-23'), 
            ('2-14-1', '2-28'),
            ('2-23', '2-27'),
            ('2-24', '2-23'),
            ('2-26', '2-23'),
            ('2-28', '2-39'),
            ('2-28', '2-47 (B)'),
            ('2-28', '2-40'),
            ('2-28', '2-41'),
            ('2-28', '2-42'),
            ('2-28', '2-00'),
            ('2-29', '2-31'),
            ('2-30', '2-28'),
            ('2-31', '2-30'),
            ('2-31', '2-28'),
            ('2-32', '2-31'),
            ('2-34', '2-28'),
            ('2-35', '2-31'),
            ('2-36', '2-31'),
            ('2-46', '2-28'),
            ('2-47 (A)', '2-28'),
            ('2-23', '2-21'),
            ('2-22', '2-23'),
            ('2-14', '2-20'),
            ('2-19', '2-14'),
            ('2-14', '2-15'),
            ('2-14', '2-16'),
            ('2-14', '2-17'),
            ('2-14', '2-18'),
            ('2-14', '2-14-1'),
            ('2-14', '2-13'),
            ('2-14', '2-12'),
            ('2-14', '2-10'),
            ('2-09', '2-10'),
            ('2-11', '2-04'),
            ('2-09', '2-04'),
            ('2-14', '2-07'),
            ('2-14', '2-08'),
            ('2-07', '2-04'),
            ('2-08', '2-04'),
            ('2-14-1', '2-06'),
            ('2-06', '2-04'),
            ('2-14-1', '2-03'),
            ('2-01', '2-28'),
            ('2-02', '2-04'),
            ('2-28', '2-04'),
            ('2-28', '2-05'),
            ('2-05', '2-04'),          
            ]

eqs = string_gen(df, inf_list)

for equation in eqs:
    print(equation)