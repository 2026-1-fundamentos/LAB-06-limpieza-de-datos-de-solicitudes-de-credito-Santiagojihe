import pandas as pd
import numpy as np
from pathlib import Path

path = Path('files/input/solicitudes_de_credito.csv')
df = pd.read_csv(path, sep=';').drop(columns=['Unnamed: 0'])

# helper
for col in ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito']:
    df[col] = df[col].astype(str).str.strip()

for col in ['sexo','tipo_de_emprendimiento','línea_credito']:
    df[col] = df[col].str.lower()

for col in ['idea_negocio','barrio']:
    df[col] = df[col].str.lower()
    df[col] = df[col].str.replace('_', ' ', regex=False)
    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
    df[col] = df[col].str.strip()

df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].replace({'nan': np.nan, '': np.nan})
df['barrio'] = df['barrio'].replace({'nan': np.nan, '': np.nan})
df['estrato'] = pd.to_numeric(df['estrato'], errors='coerce').astype('Int64')
df['comuna_ciudadano'] = pd.to_numeric(df['comuna_ciudadano'], errors='coerce')

# candidate rules
candidates = []
for drop_missing in [False, True]:
    for drop_duplicates in [False, True]:
        for subset in [None, ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','estrato','comuna_ciudadano','fecha_de_beneficio','monto_del_credito','línea_credito']]:
            t = df.copy()
            if drop_missing:
                t = t.dropna(subset=['tipo_de_emprendimiento','barrio'])
            if drop_duplicates:
                if subset is None:
                    t = t.drop_duplicates()
                else:
                    t = t.drop_duplicates(subset=subset)
            if len(t) == 10206:
                print('match rows', len(t), 'drop_missing', drop_missing, 'drop_duplicates', drop_duplicates, 'subset', subset)
                print('sexo', t['sexo'].value_counts().to_dict())
                print('tipo', t['tipo_de_emprendimiento'].value_counts().to_dict())
                print('estrato', t['estrato'].value_counts().to_dict())
                print('---')
