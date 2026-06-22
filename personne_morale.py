import pandas as pd

# Lecture des fichiers Excel
df_12 = pd.read_excel("entreprises_siren_74_V15.xlsx")
df_14 = pd.read_excel("entreprises_siren_74_V17.xlsx")

# Colonnes à récupérer depuis V14
colonnes_a_remplacer = [
    "dirigeant_nom",
    "dirigeant_prenoms",
    "dirigeant_annee_de_naissance",
    "dirigeant_date_de_naissance",
    "dirigeant_qualite",
    "dirigeant_nationalite"
]

# Création d'un dataframe contenant uniquement les colonnes utiles
df_14_infos = df_14[["siren"] + colonnes_a_remplacer]

# Fusion entre V12 et V14
df_15 = df_12.merge(
    df_14_infos,
    left_on="dirigeant_siren",
    right_on="siren",
    how="left",
    suffixes=("", "_v14")
)

# Remplacement des colonnes de V12 par celles provenant de V14
for colonne in colonnes_a_remplacer:
    df_15[colonne] = df_15[f"{colonne}_v14"]

# Suppression des colonnes temporaires
colonnes_temp = ["siren"] + [f"{col}_v14" for col in colonnes_a_remplacer]
df_15.drop(columns=colonnes_temp, inplace=True)

# Sauvegarde du fichier V15
df_15.to_excel("entreprises_siren_74_V17.xlsx", index=False)

# Sélection des dirigeants personnes morales dans V14
df_16 = df_14[
    df_14["dirigeant_type_dirigeant"].str.lower().fillna("") == "personne morale"
]

# Sauvegarde du fichier V16
df_16.to_excel("entreprises_siren_74_V19.xlsx", index=False)

print("Fichier créé : entreprises_siren_74_V15.xlsx")
print("Fichier créé : entreprises_siren_74_V16.xlsx")