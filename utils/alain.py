import pandas as pd

# =========================
# FICHIERS
# =========================
fichier_principal = "entreprises_siret_74_V3.xlsx"

fichiers_alain = [
    "fichier 74 janv 2021.xls",
    "fichier 74 dec 2024 globale pour Alain et Phonetic.xlsx",
    "Fichier 74 04-2018.xlsx"
]

# =========================
# CHARGEMENT FICHIER PRINCIPAL
# =========================
df_principal = pd.read_excel(fichier_principal, dtype=str)

# Adapter au nom réel de ta colonne SIREN
col_siren_principal = "siren"

# Création des colonnes si elles n'existent pas
if "telephone" not in df_principal.columns:
    df_principal["telephone"] = ""

if "traite" not in df_principal.columns:
    df_principal["traite"] = "non traité"

# =========================
# CHARGEMENT FICHIERS ALAIN
# =========================
liste_df = []

for fichier in fichiers_alain:
    df = pd.read_excel(fichier, dtype=str)

    # Adapter au nom réel de la colonne SIRET
    df["siren"] = df["SIRET"].str[:9]

    # Adapter au nom réel de la colonne téléphone
    df = df[["siren", "TELEPHONE"]]

    liste_df.append(df)

df_alain = pd.concat(liste_df, ignore_index=True)

# Suppression des doublons sur le siren
df_alain = df_alain.drop_duplicates(subset="siren")

print(f"Entreprises traitées par Alain : {len(df_alain)}")

# =========================
# ENTREPRISES ABSENTES
# =========================
sirens_principal = set(df_principal[col_siren_principal])

absentes = df_alain[~df_alain["siren"].isin(sirens_principal)]

print("\n=== ENTREPRISES TRAITÉES PAR ALAIN MAIS ABSENTES ===")
print(f"Nombre : {len(absentes)}")

for _, row in absentes.iterrows():
    print(
        f"SIREN : {row['siren']} | Téléphone : {row['TELEPHONE']}"
    )

# =========================
# AJOUT DES DONNÉES ALAIN
# =========================
mapping_tel = dict(
    zip(df_alain["siren"], df_alain["TELEPHONE"])
)

mask = df_principal[col_siren_principal].isin(df_alain["siren"])

df_principal.loc[mask, "telephone"] = (
    df_principal.loc[mask, col_siren_principal]
    .map(mapping_tel)
)

df_principal.loc[mask, "traite"] = "traité par Alain"

# =========================
# SAUVEGARDE
# =========================
fichier_sortie = "entreprises_74.xlsx"

df_principal.to_excel(fichier_sortie, index=False)

print("\n=== TERMINÉ ===")
print(f"Entreprises marquées : {mask.sum()}")
print(f"Fichier créé : {fichier_sortie}")