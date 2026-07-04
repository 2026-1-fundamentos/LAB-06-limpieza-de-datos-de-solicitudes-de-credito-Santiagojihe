import pandas as pd
import numpy as np
from pathlib import Path

path = Path('files/input/solicitudes_de_credito.csv')
df = pd.read_csv(path, sep=';').drop(columns=['Unnamed: 0'])

# normalize helper

def normalize_text(series):
    s = series.astype(str).str.strip()
    s = s.str.replace('_', ' ', regex=False)
    s = s.str.replace(r'\s+', ' ', regex=True)
    s = s.str.strip()
    s = s.str.lower()
    s = s.replace({'nan': np.nan, 'none': np.nan, '': np.nan})
    return s

# candidate transforms
for name, func in [
    ('raw', lambda d: d.copy()),
    ('norm', lambda d: d.assign(**{c: normalize_text(d[c]) for c in ['sexo','tipo_de_emprendimiento','idea_negocio','barrio','línea_credito']})),
]:
    t = func(df)
    # ensure numeric conversions for some
    t['estrato'] = pd.to_numeric(t['estrato'], errors='coerce')
    t['comuna_ciudadano'] = pd.to_numeric(t['comuna_ciudadano'], errors='coerce')
    # drop duplicates maybe to be tested later
    for dropna, dropdup, label in [
        (False, False, 'none'),
        (True, False, 'dropna'),
        (True, True, 'dropna_dup'),
    ]:
        tt = t.copy()
        if dropna:
            tt = tt.dropna(subset=['tipo_de_emprendimiento','barrio'])
        if dropdup:
            tt = tt.drop_duplicates()
        # further filters
        for filt_name, mask in [
            ('none', pd.Series(True, index=tt.index)),
            ('valid_line', tt['línea_credito'].isin(['microempresarial','agropecuaria','credioportuno'])),
            ('valid_type', tt['tipo_de_emprendimiento'].isin(['comercio','servicio','industria','agropecuaria'])),
            ('valid_type_line', tt['tipo_de_emprendimiento'].isin(['comercio','servicio','industria','agropecuaria']) & tt['línea_credito'].isin(['microempresarial','agropecuaria','credioportuno'])),
            ('valid_type_line_sex', tt['tipo_de_emprendimiento'].isin(['comercio','servicio','industria','agropecuaria']) & tt['línea_credito'].isin(['microempresarial','agropecuaria','credioportuno']) & tt['sexo'].isin(['masculino','femenino'])),
        ]:
            ttt = tt.loc[mask].copy()
            if ttt.empty:
                continue
            print(name, label, filt_name, 'rows', len(ttt))
            print('sexo', ttt['sexo'].value_counts().to_dict())
            print('tipo', ttt['tipo_de_emprendimiento'].value_counts().to_dict())
            print('estrato', ttt['estrato'].value_counts().to_dict())
            print('line', ttt['línea_credito'].value_counts().to_dict())
            print('---')
            break
        print('====')
