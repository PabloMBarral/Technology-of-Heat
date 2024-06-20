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
# Temperature conversion

def converttemp(t, base_in='C', base_out='K'):
    if base_in=='C' and base_out=='K':
        return t+273.15
# -----------------------------------------


# -----------------------------------------
# Data

    # Environment

t_0 = 15 # C
T_0 = converttemp(base_in='C', base_out='K', t=t_0) # K
p_0 = 101.325 # kPa(a)

    # 3.11 Combustion reference conditions
    #   Specified temperature , t1, and pressure, p1, at which the fuel is notionally burned. In calorific value calculations, products of combustion are at the same temperature than gas + oxygen.
    #   t_1 can only belong to a predefined set of values (0 C, 15 C, 15.55 C (meaning 60 F), 20 C, 25 C).


t_1 = 25 # C
T_1 = converttemp(base_in='C', base_out='K', t=t_1) # K
p_1 = 101.325 # kPa(a)

    # 3.12 Metering reference conditions
    #   Specified temperature , t2, and pressure, p2, at which the volume of fuel to be burned is notionally determined. 
    #   Note 1 to entry: There is no a priori reason for the metering reference conditions to be the same as the combustion reference conditions (see Figure 1) .
    #   t_2 can only belong to a predefined set of values (0 C, 15 C, 15.55 C (meaning 60 F), 20 C).

    # The summation is taken over all N components of the mixture and the formula is valid for the range 90 < p2/kPa < 110.


t_2 = 15 # C
T_2 = converttemp(base_in='C', base_out='K', t=t_2) # K
p_2 = 101.325 # kPa(a)
# -----------------------------------------


# -----------------------------------------
# File path

main_path = os.path.dirname(os.path.abspath(__file__))
# -----------------------------------------


# -----------------------------------------
#Load and process csv files

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
    'gross_calorific_value.csv': ['component', 'Hc_0_G_j_0', 'Hc_0_G_j_15', 'Hc_0_G_j_15_55', 'Hc_0_G_j_20', 'Hc_0_G_j_25', 'u_Hc_j'],
}

# File processing
dataframes = {}
arrays = {}

for file, columns in files_and_columns.items():
    file_path = os.path.join(main_path, file)
    df, arr = load_and_process_csv(file_path, columns)
    dataframes[file] = df
    arrays[file] = arr
# -----------------------------------------


# -----------------------------------------
# User input - Mole fractions.
# [dim]

x_j = arrays['molar_fraction.csv']['x_j'] # Array. User input. csv file: component_j & x_j.
# -----------------------------------------


# -----------------------------------------
# Table 2 — Summation factors for components of natural gas at various metering reference temperatures, and standard uncertainty.
# [dim]
# All values refer to a pressure p_0 = 101.325 kPa(a).


if t_2 == 0:
    s_j = arrays['summation_factor.csv']['s_j_0'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
elif t_2 == 15:
    s_j = arrays['summation_factor.csv']['s_j_15'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
elif t_2 == 15.55:
    s_j = arrays['summation_factor.csv']['s_j_15_55'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
elif t_2 == 20:
    s_j = arrays['summation_factor.csv']['s_j_20'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.

u_s_j = arrays['summation_factor.csv']['u_s_j'] # Array. Summation factors. Table 2. csv file: component_j & s_j_0 & s_j_15 & s_j_15_55 & s_j_20 & u_s_j.
# -----------------------------------------


# -----------------------------------------
# Formula (1) - Compression factor.

Z = 1 - (p_2 / p_0) * (x_j @ s_j)**2 # [dim]
# -----------------------------------------


# -----------------------------------------
# Table 3 — Gross calorific values on a molar basis for components of natural gas in the ideal gas state at various combustion reference temperatures, and standard uncertainty.
# [kJ/mol]

if t_1 == 0:
    Hc_0_G_j = arrays['gross_calorific_value.csv']['Hc_0_G_j_0'] # Array. Gross calorific values. Table 3. csv file: component_j & Hc_0_G_j_0 & Hc_0_G_j_15 & Hc_0_G_j_15_55 & Hc_0_G_j_20 & Hc_0_G_j_25 & u_Hc_j.
elif t_1 == 15:
    Hc_0_G_j = arrays['gross_calorific_value.csv']['Hc_0_Gj_15'] # Array. Gross calorific values. Table 3. csv file: component_j & Hc_0_G_j_0 & Hc_0_G_j_15 & Hc_0_G_j_15_55 & Hc_0_G_j_20 & Hc_0_G_j_25 & u_Hc_j.
elif t_1 == 15.55:
    Hc_0_G_j = arrays['gross_calorific_value.csv']['Hc_0_G_j_15_55'] #  Array. Gross calorific values. Table 3. csv file: component_j & Hc_0_G_j_0 & Hc_0_G_j_15 & Hc_0_G_j_15_55 & Hc_0_G_j_20 & Hc_0_G_j_25 & u_Hc_j.
elif t_1 == 20:
    Hc_0_G_j = arrays['gross_calorific_value.csv']['Hc_0_G_j_20'] # Array. Gross calorific values. Table 3. csv file: component_j & Hc_0_G_j_0 & Hc_0_G_j_15 & Hc_0_G_j_15_55 & Hc_0_G_j_20 & Hc_0_G_j_25 & u_Hc_j.
elif t_1 == 25:
    Hc_0_G_j = arrays['gross_calorific_value.csv']['Hc_0_G_j_25'] # Array. Gross calorific values. Table 3. csv file: component_j & Hc_0_G_j_0 & Hc_0_G_j_15 & Hc_0_G_j_15_55 & Hc_0_G_j_20 & Hc_0_G_j_25 & u_Hc_j.

u_Hc = arrays['gross_calorific_value.csv']['u_Hc_j'] # Array. Gross calorific values. Table 3. csv file: component_j & Hc_0_G_j_0 & Hc_0_G_j_15 & Hc_0_G_j_15_55 & Hc_0_G_j_20 & Hc_0_G_j_25 & u_Hc_j.
# -----------------------------------------


# -----------------------------------------
# Formula (2) - Gross calorific value. Volume basis.
# Ideal-gas gross calorific value: Hc_0_G
# Real-gas gross calorific value: Hc_G

Hc_0_G = x_j @ Hc_0_G_j # [kJ/mol]
Hc_G = Hc_0_G           # [kJ/mol]
# -----------------------------------------


# -----------------------------------------
# Table 1 — Molar mass and atomic indices for components of natural gas.
# M_j [kg/kmol]
# a_j, b_j, c_j, d_j, e_j [dim]

M_j = arrays['molar_mass.csv']['M_j'] # Array. Molar mass. Table 1. csv file: component_j & M_j.

a_j = arrays['atomic_index.csv']['a_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
b_j = arrays['atomic_index.csv']['b_j'] # Array. Atomic index (CHNOS). Table 1. csv file: omponent_j & a_j & b_j & c_j & d_j & e_j.
c_j = arrays['atomic_index.csv']['c_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
d_j = arrays['atomic_index.csv']['d_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
e_j = arrays['atomic_index.csv']['e_j'] # Array. Atomic index (CHNOS). Table 1. csv file: component_j & a_j & b_j & c_j & d_j & e_j.
# -----------------------------------------


# -----------------------------------------
# Table A.5 — Standard enthalpy of vaporization of water, and standard uncertainty.
# [kJ/mol]

if t_1 == 0:
    L_0_j = 45.064 # [kJ/mol]
elif t_1 == 15:
    L_0_j = 44.431 # [kJ/mol]
elif t_1 == 15.55:
    L_0_j = 44.408 # [kJ/mol]
elif t_1 == 20:
    L_0_j = 44.222 # [kJ/mol]
elif t_1 == 25:
    L_0_j = 44.013 # [kJ/mol]

u_L_0 = 0.004 # [kJ/mol]
# -----------------------------------------


# -----------------------------------------
# Formula (3) - Net calorific value. Volume basis.
# Ideal-gas net calorific value: Hc_0_N
# Real-gas net calorific value: Hc_N

Hc_0_N = Hc_0_G - (x_j @ b_j) / 2 * L_0_j #kJ/mol
Hc_N = Hc_0_N           # [kJ/mol]
# -----------------------------------------

# -----------------------------------------
# Formula (5) - Molar mass.

M = M_j @ x_j # kg/kmol
# -----------------------------------------


# -----------------------------------------
# Formula (4) - Gross calorific value. Mass basis.
# Ideal-gas gross calorific value: Hm_0_G
# Real-gas gross calorific value: Hm_G

Hm_0_G = Hc_0_G / M # kJ/kg
Hm_G = Hm_0_G       # kJ/kg
# -----------------------------------------


# -----------------------------------------
# Formula (6) - Net calorific value. Mass basis.
# Ideal-gas net calorific value: Hm_0_N
# Real-gas net calorific value: Hm_N

Hm_0_N = Hc_0_N / M # kJ/kg
Hm_N = Hm_0_N       # kJ/kg
# -----------------------------------------


# -----------------------------------------
# Table A.1 — Molar gas constant.
# [kJ/kmol-K] or [J/mol-K]

R = 8.3144621   # [kJ/kmol-K] or [J/mol-K]
u_R = 0.0000075 # [kJ/kmol-K] or [J/mol-K]
# -----------------------------------------


# -----------------------------------------
V_0 = R * T_2 / p_2 / 1000  # m³/mol
V = Z * V_0                 # m³/mol               


Hv_0_G = Hc_0_G / V_0 # kJ/m³
Hv_0_N = Hc_0_N / V_0 # kJ/m³

Hv_G = Hc_0_G / V # kJ/m³
Hv_N = Hc_0_N / V # kJ/m³