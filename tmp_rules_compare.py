import pandas as pd
import numpy as np
from pathlib import Path

path = Path('files/input/solicitudes_de_credito.csv')
df = pd.read_csv(path, sep=';').drop(columns=['Unnamed: 0'])

# baseline normalize
base = df.copy()
for col in ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito']:
    base[col] = base[col].astype(str).str.strip()
for col in ['sexo','tipo_de_emprendimiento','línea_credito']:
    base[col] = base[col].str.lower()
for col in ['idea_negocio','barrio']:
    base[col] = base[col].str.lower()
    base[col] = base[col].str.replace('_', ' ', regex=False)
    base[col] = base[col].str.replace(r'\s+', ' ', regex=True)
    base[col] = base[col].str.strip()
base['tipo_de_emprendimiento'] = base['tipo_de_emprendimiento'].replace({'nan': np.nan, '': np.nan})
base['barrio'] = base['barrio'].replace({'nan': np.nan, '': np.nan})

# variant 1: dropna on type+barrio, drop_duplicates all cols
v1 = base.dropna(subset=['tipo_de_emprendimiento', 'barrio']).drop_duplicates()
# variant 2: dropna on type+barrio and duplicates on subset cols
subset_cols = ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','fecha_de_beneficio','monto_del_credito','línea_credito']
v2 = base.dropna(subset=['tipo_de_emprendimiento', 'barrio']).drop_duplicates(subset=subset_cols)
# variant 3: dropna on type+barrio and drop duplicated columns only in selected cols but maybe use only no lowercase? no
v3 = base.dropna(subset=['tipo_de_emprendimiento', 'barrio']).drop_duplicates(subset=['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','fecha_de_beneficio','línea_credito'])

for name, t in [('v1', v1), ('v2', v2), ('v3', v3)]:
    print(name, 'rows', len(t))
    print('sexo', t['sexo'].value_counts().to_dict())
    print('tipo', t['tipo_de_emprendimiento'].value_counts().to_dict())
    print('---')
