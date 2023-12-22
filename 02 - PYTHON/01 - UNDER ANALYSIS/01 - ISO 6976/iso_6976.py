import pandas as pd
import os
import cirpy
# import chemicals

# General
main_path = os.path.dirname(os.path.abspath(__file__))

# Molar mass
Molar_mass_path = os.path.join(main_path, 'Molar_mass.csv')

Molar_mass = pd.read_csv(Molar_mass_path, header=None, sep=';')

Molar_mass.columns = ['component', 'Molar mass']
Molar_mass['component'] = Molar_mass['component'].str.replace('_', ',')


# Molar fraction
Molar_fraction_path = os.path.join(main_path, 'Molar_fraction.csv')

Molar_fraction = pd.read_csv(Molar_fraction_path, header=None, sep=';')

Molar_fraction.columns = ['component', 'Molar fraction']
Molar_fraction['component'] = Molar_fraction['component'].str.replace('_', ',')

# Output
print(Molar_mass)
print(Molar_fraction)


# cas = pd.DataFrame(Molar_mass.iloc[:, 0], columns=['component'])
# cas['cas'] = cas['component'].apply(lambda x: cirpy.resolve(x, 'cas') if pd.notnull(x) else None)

# perhaps we should generate a j file with the iso-index. Just in case.










# Draft
# cas_2 = pd.DataFrame(Molar_mass.iloc[:, 0], columns=['component'])
# cas_2['cas'] = cas['component'].apply(lambda x: chemicals.identifiers.CAS_from_any(x, autoload=False, cache=True) if pd.notnull(x) else None)
