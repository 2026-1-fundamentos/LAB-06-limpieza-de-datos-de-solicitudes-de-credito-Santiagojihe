import pandas as pd
import numpy as np
from pathlib import Path

path = Path('files/input/solicitudes_de_credito.csv')
df = pd.read_csv(path, sep=';')
df = df.drop(columns=['Unnamed: 0'])

# normalize text
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].replace({'nan': np.nan, 'none': np.nan})

# clean idea_negocio and barrio spacing
for col in ['idea_negocio', 'barrio']:
    df[col] = df[col].astype(str).str.replace('_', ' ', regex=False)
    df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
    df[col] = df[col].str.strip()

# maybe remove rows with missing in critical cols
# df = df.dropna(subset=['tipo_de_emprendimiento', 'barrio'])

df2 = df.drop_duplicates()
print('rows', len(df2))
print('sexo')
print(df2['sexo'].value_counts().to_string())
print('tipo')
print(df2['tipo_de_emprendimiento'].value_counts().to_string())
print('idea head')
print(df2['idea_negocio'].value_counts().head(20).to_string())
print('barrio head')
print(df2['barrio'].value_counts().head(20).to_string())
print('estrato')
print(df2['estrato'].value_counts().to_string())
print('comuna')
print(df2['comuna_ciudadano'].value_counts().head(20).to_string())
