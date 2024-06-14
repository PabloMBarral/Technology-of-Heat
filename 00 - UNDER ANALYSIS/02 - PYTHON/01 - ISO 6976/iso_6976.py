# -----------------------------------------

import os

import numpy as np
import pandas as pd
# -----------------------------------------


# -----------------------------------------
'General notes'

"""
    Std inputs are in the accompaning csv files, except por L_0, R, which are included in this script.
    This script is based on the 2016 version of the ISO 6976 standard. If a new version, this code needs updating.

    A possible upgrade is to interpolate calorific values for t1 values different from the preset ones.

    For the purposes of this script, th is calculation (formula (11)) is only valid for Z > 0 ,9.

    Formula (1) -Z(t2, p2)- can also be used to calculate values of compression factor of pure components , but this will not necessarily give the most accurate result possible.
    In particular, the formula will not provide a value for the compression factor of hydrogen , helium or neon, for which Z > 1, nor for any components, such as the higher hydrocarbons, that are not gaseous at the metering reference conditions. The user should consider the fitness-for-purpose of any such calculation before its use outside of the context of the script.
"""
# -----------------------------------------


# -----------------------------------------
'Data'

    # Environment

t_0 = 15 # C
p_0 = 101.325 # kPa(a)

    # 3.11 Combustion reference conditions
    #   Specified temperature , t1, and pressure, p1, at which the fuel is notionally burned. In calorific value calculations, products of combustion are at the same temperature than gas + oxygen.
    #   t_1 can only belong to a predefined set of values (0 C, 15 C, 15.55 C (meaning 60 F), 20 C, 25 C).


t_1 = 25 # C
p_1 = 101.325 # kPa(a)

    # 3.12 Metering reference conditions
    #   Specified temperature , t2, and pressure, p2, at which the volume of fuel to be burned is notionally determined. 
    #   Note 1 to entry: There is no a priori reason for the metering reference conditions to be the same as the combustion reference conditions (see Figure 1) .
    #   t_2 can only belong to a predefined set of values (0 C, 15 C, 15.55 C (meaning 60 F), 20 C).

    # The summation is taken over all N components of the mixture and the formula is valid for the range 90 < p2/kPa < 110.


t_2 = 15 # C
p_2 = 101.325 # kPa(a)
# -----------------------------------------


# -----------------------------------------
'File path'

main_path = os.path.dirname(os.path.abspath(__file__))
# -----------------------------------------


# -----------------------------------------
'Load and process csv files'

def load_and_process_csv(file_path: str, columns: list, sep: str=';', replace_char: str='_', new_char: str=',') -> tuple:
    """
    Load a CSV file, assign column names, and replace characters in the 'component' column.

    Args:
        file_path (str): Path to the CSV file.
        columns (list): List of column names.
        sep (str): Field separator in the CSV. A default value is ';'.
        replace_char (str): Character to replace in the 'component' column. A default value is '_'.
        new_char (str): New character to replace the old one in the 'component' column. A default value is ','.

    Returns:
        tuple: Tuple of processed DataFrames and numpy arrays.
    """

    df = pd.read_csv(file_path, header=None, sep=sep)
    df.columns = columns
    df['component'] = df['component'].str.replace(replace_char, new_char)
    
    # Extract numpy arrays
    arrays = {col: df[col].to_numpy() for col in columns[1:]}
    
    return df, arrays

# Define the corresponding files and columns
files_and_columns = {
    'molar_fraction.csv': ['component', 'x_j'],
    'molar_mass.csv': ['component', 'M_j'],
    'atomic_index.csv': ['component', 'a_j', 'b_j', 'c_j', 'd_j', 'e_j'],
    'summation_factor.csv': ['component', 's_j_0', 's_j_15', 's_j_15_55', 's_j_20', 'u_s_j'],
}

# File processing
dataframes = {}
arrays = {}

for file, columns in files_and_columns.items():
    file_path = os.path.join(main_path, file)
    df, arr = load_and_process_csv(file_path, columns)
    dataframes[file] = df
    arrays[file] = arr

# Acessing arrays
x_j = arrays['molar_fraction.csv']['x_j'] # Array. User input. csv file: component_j & x_j.

if t_2 == 0:
    s_j_0 = arrays['summation_factor.csv']['s_j_0'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
    s_j = s_j_0
elif t_2 == 15:
    s_j_15 = arrays['summation_factor.csv']['s_j_15'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
    s_j = s_j_15
elif t_2 == 15.55:
    s_j_15_55 = arrays['summation_factor.csv']['s_j_15_55'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
    s_j = s_j_15_55
elif t_2 == 20:
    s_j_20 = arrays['summation_factor.csv']['s_j_20'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
    s_j = s_j_20

u_s_j = arrays['summation_factor.csv']['u_s_j'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.


M_j = arrays['molar_mass.csv']['M_j'] # Array. Molar mass. Table 1. csv file: component_j & M_j.

a_j = arrays['atomic_index.csv']['a_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
b_j = arrays['atomic_index.csv']['b_j'] # Array. Atomic index (CHNOS). Table 1. csv file: omponent_j & a_j & b_j & c_j & d_j & e_j.
c_j = arrays['atomic_index.csv']['c_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
d_j = arrays['atomic_index.csv']['d_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
e_j = arrays['atomic_index.csv']['e_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
# -----------------------------------------


# -----------------------------------------
# Formula (1)

Z = 1 - (p_2 / p_0) * (x_j @ s_j)**2
# -----------------------------------------