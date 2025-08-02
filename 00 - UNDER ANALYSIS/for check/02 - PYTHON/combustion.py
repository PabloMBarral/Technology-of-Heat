import chemicals as ch
import numpy as np

nitrogen = {'name': 'nitrogen',
            'CAS': '7727-37-9',
            'atoms': ch.simple_formula_parser('N2'),
            'MW': ch.molecular_weight(ch.simple_formula_parser('N2')),
            'y_air': 0.59,
            'y_fuel': 0.0342,
            }

oxygen = {'name': 'oxygen',
          'CAS': '7782-44-7',
          'atoms': ch.simple_formula_parser('O2'),
          'MW': ch.molecular_weight(ch.simple_formula_parser('O2')),
          'y_air': 0.21,
          'y_fuel': 0,
          }

water = {'name': 'water',
         'CAS': '7732-18-5',
         'atoms': ch.simple_formula_parser('H2O'),
         'MW': ch.molecular_weight(ch.simple_formula_parser('H2O')),
         'y_air': 0.0,
         'y_fuel': 0,
         }

carbon_dioxide = {'name': 'carbon dioxide',
                  'CAS': '124-38-9',
                  'atoms': ch.simple_formula_parser('CO2'),
                  'MW': ch.molecular_weight(ch.simple_formula_parser('CO2')),
                  'y_air': 0.1,
                  'y_fuel': 0.0024,
                  }

argon = {'name': 'argon',
          'CAS': '7440-37-1',
          'atoms': ch.simple_formula_parser('Ar'),
          'MW': ch.molecular_weight(ch.simple_formula_parser('Ar')),
          'y_air': 0.1,
          'y_fuel': 0,
          }

methane = {'name': 'methane',
           'CAS': '74-82-8',
           'atoms': ch.simple_formula_parser('CH4'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('CH4')),
           'y_air': 0,
           'y_fuel': 0.9008,
           }

ethane = {'name': 'ethane',
          'CAS': '74-84-0',
          'atoms': ch.simple_formula_parser('C2H6'),
          'MW': ch.molecular_weight(ch.simple_formula_parser('C2H6')),
          'y_air': 0,
          'y_fuel': 0.0473,
          }

propane = {'name': 'propane',
           'CAS' : '74-98-6',
           'atoms': ch.simple_formula_parser('C3H8'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C3H8')),
           'y_air': 0,
           'y_fuel': 0.0123,
           }

n_butane = {'name': 'n-butane',
           'CAS' : '106-97-8',
           'atoms': ch.simple_formula_parser('C4H10'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C4H10')),
           'y_air': 0,
           'y_fuel': 0.0024,
           }

n_pentane = {'name': 'n-pentane',
           'CAS' : '109-66-0',
           'atoms': ch.simple_formula_parser('C5H12'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C5H12')),
           'y_air': 0,
           'y_fuel': 0.0006,
           }

n_hexane = {'name': 'n-hexane',
           'CAS' : '110-54-3',
           'atoms': ch.simple_formula_parser('C6H14'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C6H14')),
           'y_air': 0,
           'y_fuel': 0.,
           }

n_heptane = {'name': 'n-heptane',
           'CAS' : '142-82-5',
           'atoms': ch.simple_formula_parser('C7H16'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C7H16')),
           'y_air': 0,
           'y_fuel': 0.,
           }

n_octane = {'name': 'n-octane',
           'CAS' : '111-65-9',
           'atoms': ch.simple_formula_parser('C8H18'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C8H18')),
           'y_air': 0,
           'y_fuel': 0.,
           }

n_nonane = {'name': 'n-nonane',
           'CAS' : '111-84-2',
           'atoms': ch.simple_formula_parser('C9H20'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C9H20')),
           'y_air': 0,
           'y_fuel': 0.,
           }

n_decane = {'name': 'n-decane',
           'CAS' : '124-18-5',
           'atoms': ch.simple_formula_parser('C10H22'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C10H22')),
           'y_air': 0,
           'y_fuel': 0.,
           }

i_butane = {'name': '2-methylpropane / i-butane',
           'CAS' : '75-28-5',
           'atoms': ch.simple_formula_parser('C4H10'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C4H10')),
           'y_air': 0,
           'y_fuel': 0.,
           }

i_pentane = {'name': '2-methylbutane / i-pentane',
           'CAS' : '78-78-4',
           'atoms': ch.simple_formula_parser('C5H12'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C5H12')),
           'y_air': 0,
           'y_fuel': 0.,
           }

ethylene = {'name': 'ethylene / ethene',
           'CAS' : '74-85-1',
           'atoms': ch.simple_formula_parser('C2H4'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C2H4')),
           'y_air': 0,
           'y_fuel': 0.,
           }

propylene = {'name': 'propylene / propene',
           'CAS' : '115-07-1',
           'atoms': ch.simple_formula_parser('C3H6'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C3H6')),
           'y_air': 0,
           'y_fuel': 0.,
           }

_1_butylene = {'name': '1-butylene / 1-butene',
           'CAS' : '106-98-9',
           'atoms': ch.simple_formula_parser('C4H8'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C4H8')),
           'y_air': 0,
           'y_fuel': 0.,
           }

cis_2_butylene = {'name': 'cis-2-butylene / cis-2-butene',
           'CAS' : '590-18-1',
           'atoms': ch.simple_formula_parser('C4H8'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C4H8')),
           'y_air': 0,
           'y_fuel': 0.,
           }

trans_2_butylene = {'name': 'trans-2-butylene / trans-2-butene',
           'CAS' : '624-64-6',
           'atoms': ch.simple_formula_parser('C4H8'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C4H8')),
           'y_air': 0,
           'y_fuel': 0.,
           }

i_butylene = {'name': 'i-butylene / i-butene',
           'CAS' : '115-11-7',
           'atoms': ch.simple_formula_parser('C4H8'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C4H8')),
           'y_air': 0,
           'y_fuel': 0.,
           }

_1_pentene = {'name': '1-pentene',
           'CAS' : '109-67-1',
           'atoms': ch.simple_formula_parser('C5H10'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('C5H10')),
           'y_air': 0,
           'y_fuel': 0.,
           }

carbon_monoxide = {'name': 'carbon monoxide',
           'CAS' : '630-08-0',
           'atoms': ch.simple_formula_parser('CO'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('CO')),
           'y_air': 0,
           'y_fuel': 0.,
           }

hydrogen = {'name': 'hydrogen',
           'CAS' : '1333-74-0',
           'atoms': ch.simple_formula_parser('H2'),
           'MW': ch.molecular_weight(ch.simple_formula_parser('H2')),
           'y_air': 0,
           'y_fuel': 0.,
           }

substances = [nitrogen,
              oxygen,
              water,
              carbon_dioxide,
              argon,
              methane,
              ethane,
              propane,
              n_butane,
              n_pentane,
              n_hexane,
              n_heptane,
              n_octane,
              n_nonane,
              n_decane,
              i_butane,
              i_pentane,
              ethylene,
              propylene,
              _1_butylene,
              cis_2_butylene,
              trans_2_butylene,
              i_butylene,
              _1_pentene,
              carbon_monoxide,
              hydrogen]

names = [substances[i]['name'] for i in range(len(substances))]
MW = [substances[i]['MW'] for i in range(len(substances))]
CAS = [substances[i]['CAS'] for i in range(len(substances))]
atoms = [substances[i]['atoms'] for i in range(len(substances))]
zs_air = [substances[i]['y_air'] for i in range(len(substances))]
zs_fuel = [substances[i]['y_fuel'] for i in range(len(substances))]

n_fuel = 1.0     #Caudal molar en mol/s. Podemos cambiar la base para ponerlo en kg.
O2_excess = 4#0.18  #Exceso de aire.

ans = ch.fuel_air_spec_solver(zs_air = zs_air,
                              zs_fuel = zs_fuel,
                              CASs = CAS,
                              atomss = atoms,
                              n_fuel = n_fuel,
                              O2_excess = O2_excess)

MW_air = np.dot(np.array(MW), np.array(zs_air))
MW_fuel = np.dot(np.array(MW), np.array(zs_fuel))
MW_gases = np.dot(np.array(MW), np.array(ans['zs_out']))

[round(i, 5) for i in ans['zs_out']] #Redondeamos las fracciones molares de los gases de combustión.

print(ans)