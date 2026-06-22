import pandas as pd

# Lecture des fichiers
df_v10 = pd.read_excel("entreprises_siren_74_V10.xlsx")
df_v11 = pd.read_excel("entreprises_siren_74_V11.xlsx")
df_v13 = pd.read_excel("entreprises_siren_74_V13.xlsx")
df_v14 = pd.read_excel("entreprises_siren_74_V14.xlsx")

# Fusion des données
df = pd.concat([df_v10, df_v11, df_v13, df_v14], ignore_index=True)

# Remplacement des valeurs vides par "Personne morale"
df["dirigeant_type_dirigeant"] = (
    df["dirigeant_type_dirigeant"]
    .fillna("Personne morale")
    .replace("", "Personne morale")
    .astype(str)
    .str.strip()
)

# Les chaînes vides après strip deviennent aussi "Personne morale"
df.loc[
    df["dirigeant_type_dirigeant"] == "",
    "dirigeant_type_dirigeant"
] = "Personne morale"

# Séparation
df_pp = df[
    df["dirigeant_type_dirigeant"].str.lower() == "personne physique"
]

df_pm = df[
    df["dirigeant_type_dirigeant"].str.lower() != "personne physique"
]

# Export
df_pp.to_excel("entreprises_siren_74_V12pp.xlsx", index=False)
df_pm.to_excel("entreprises_siren_74_V12pm.xlsx", index=False)

print(f"Personnes physiques : {len(df_pp)} lignes")
print(f"Personnes morales   : {len(df_pm)} lignes")
print("Traitement terminé.")