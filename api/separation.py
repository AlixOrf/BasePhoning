import pandas as pd

# Lecture des fichiers
df_v1 = pd.read_excel("entreprises_siren_95_V1.xlsx")
df_v2 = pd.read_excel("entreprises_siren_95_V2.xlsx")
df_v3 = pd.read_excel("entreprises_siren_95_V3.xlsx")
df_v4 = pd.read_excel("entreprises_siren_95_V4.xlsx")

# Fusion des données
df = pd.concat([df_v1, df_v2, df_v3, df_v4], ignore_index=True)

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
df_pp.to_excel("entreprises_siren_95_V5pp.xlsx", index=False)
df_pm.to_excel("entreprises_siren_95_V5pm.xlsx", index=False)

print(f"Personnes physiques : {len(df_pp)} lignes")
print(f"Personnes morales   : {len(df_pm)} lignes")
print("Traitement terminé.")