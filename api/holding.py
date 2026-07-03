import requests
import pandas as pd
from pandas import json_normalize
import time

# =========================
# PARAMÈTRES
# =========================

FICHIER_ENTREE = "entreprises_siren_74_V5pm.xlsx"
FICHIER_SORTIE = "entreprises_siren_74_V6.xlsx"
MAX_TOURS = 10

base_url = "https://recherche-entreprises.api.gouv.fr/search"
headers = {"accept": "application/json"}

# =========================
# CHARGEMENT DES DONNÉES
# =========================

df_principal = pd.read_excel(FICHIER_ENTREE)
if "dernier_dirigeant_siren_pm" not in df_principal.columns:
    df_principal["dernier_dirigeant_siren_pm"] = None

if "dernier_dirigeant_denomination_pm" not in df_principal.columns:
    df_principal["dernier_dirigeant_denomination_pm"] = None

colonnes_dirigeant = [
    "dirigeant_nom",
    "dirigeant_prenoms",
    "dirigeant_annee_de_naissance",
    "dirigeant_date_de_naissance",
    "dirigeant_qualite",
    "dirigeant_nationalite",
    "dirigeant_siren",
    "dirigeant_denomination",
    "dirigeant_type_dirigeant"
]

for col in colonnes_dirigeant:
    if col in df_principal.columns:
        df_principal[col] = df_principal[col].astype("object")

# Uniformisation du SIREN dirigeant
df_principal["dirigeant_siren"] = (
    df_principal["dirigeant_siren"]
    .fillna("")
    .astype(str)
    .str.replace(".0", "", regex=False)
)

# =========================
# BOUCLE PRINCIPALE
# =========================

tour = 1

while tour <= MAX_TOURS:

    print(f"\n----- TOUR {tour}/{MAX_TOURS} -----")

    # Sélection des personnes morales restantes
    masque_pm = (
        df_principal["dirigeant_type_dirigeant"]
        .fillna("")
        .str.lower()
        .eq("personne morale")
    )

    nb_pm = masque_pm.sum()

    print(f"{nb_pm} personnes morales restantes")

    # Arrêt si plus aucune personne morale
    if nb_pm == 0:
        print("Plus aucune personne morale à traiter.")
        break

    # Liste unique des SIREN à rechercher
    sirens = (
        df_principal.loc[masque_pm, "dirigeant_siren"]
        .dropna()
        .astype(str)
        .str.replace(".0", "", regex=False)
        .unique()
    )

    all_results = []

    for i, siren in enumerate(sirens, start=1):

        print(f"{i}/{len(sirens)} : {siren}")

        try:

            r = requests.get(
                base_url,
                headers=headers,
                params={"q": siren},
                timeout=20
            )

            if r.status_code != 200:
                print(f"Erreur HTTP {r.status_code}")
                continue

            results = r.json().get("results", [])

            if results:
                all_results.append(results[0])

            time.sleep(0.2)

        except Exception as e:
            print(f"Erreur sur {siren} : {e}")

    if not all_results:
        print("Aucun résultat trouvé.")
        break

    # =========================
    # TRANSFORMATION DES RÉSULTATS
    # =========================

    df_raw = pd.DataFrame(all_results)

    if "dirigeants" in df_raw.columns:

        df_raw = df_raw.explode("dirigeants").reset_index(drop=True)

        dirigeants_df = json_normalize(
            df_raw["dirigeants"].apply(
                lambda x: x if isinstance(x, dict) else {}
            )
        ).add_prefix("dirigeant_")

        df_raw = pd.concat(
            [df_raw.drop(columns=["dirigeants"]), dirigeants_df],
            axis=1
        )

    colonnes_utiles = [
        "siren",
        "dirigeant_nom",
        "dirigeant_prenoms",
        "dirigeant_annee_de_naissance",
        "dirigeant_date_de_naissance",
        "dirigeant_qualite",
        "dirigeant_nationalite",
        "dirigeant_siren",
        "dirigeant_type_dirigeant"
    ]

    colonnes_existantes = [
        c for c in colonnes_utiles
        if c in df_raw.columns
    ]

    df_infos = df_raw[colonnes_existantes].copy()

    # Uniformisation du SIREN
    df_infos["siren"] = (
        df_infos["siren"]
        .fillna("")
        .astype(str)
        .str.replace(".0", "", regex=False)
    )

    # Dictionnaire de correspondance
    infos_dict = (
        df_infos
        .drop_duplicates(subset="siren")
        .set_index("siren")
        .to_dict("index")
    )

    # =========================
    # MISE À JOUR DES DONNÉES
    # =========================

    for index, row in df_principal.loc[masque_pm].iterrows():

        siren = row["dirigeant_siren"]

        if siren not in infos_dict:
            continue

        infos = infos_dict[siren]

        for colonne in colonnes_dirigeant:

            if colonne in infos:
                df_principal.at[index, colonne] = infos[colonne]

    tour += 1

# =========================
# FIN DE TRAITEMENT
# =========================

if tour > MAX_TOURS:
    print(f"\nLimite de {MAX_TOURS} tours atteinte.")

# Export final
df_principal.to_excel(
    FICHIER_SORTIE,
    index=False
)

print("\nTerminé.")
print(f"Fichier créé : {FICHIER_SORTIE}")