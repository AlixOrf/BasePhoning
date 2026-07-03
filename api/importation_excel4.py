import requests
import pandas as pd
from pandas import json_normalize
import time

# Ici les éléments que je filtre pour récupérer mes données
base_url = "https://recherche-entreprises.api.gouv.fr/search"
params = {
    "departement": "74", # Le département, pas compliqué
    "etat_administratif": "A", # Si l'entreprise est active où non
    "est_association": "false", # Si ce n'est pas une assosiation (revérifier derrière)
    "activite_principale": "01.11Z, 01.12Z, 01.13Z, 01.14Z, 01.15Z, 01.16Z, 01.19Z, 01.21Z, 01.22Z, 01.23Z, 01.24Z, 01.25Z, 01.26Z, 01.27Z, 01.28Z, 01.29Z, 01.30Z, 01.41Z, 01.42Z, 01.43Z, 01.44Z, 01.45Z, 01.46Z, 01.47Z, 01.49Z, 01.50Z, 01.61Z, 01.62Z, 01.63Z, 01.64Z, 01.70Z,02.10Z, 02.20Z, 02.30Z, 02.40Z,03.11Z, 03.12Z, 03.21Z, 03.22Z,05.10Z, 05.20Z,06.10Z, 06.20Z,07.10Z, 07.21Z, 07.29Z,08.11Z, 08.12Z, 08.91Z, 08.92Z, 08.93Z, 08.99Z,12.00Z,19.10Z, 19.20Z,35.11Z, 35.12Z, 35.13Z, 35.14Z, 35.21Z, 35.22Z, 35.23Z, 35.30Z,36.00Z,37.00Z,38.11Z, 38.12Z, 38.21Z, 38.22Z, 38.31Z, 38.32Z,39.00Z,45.11Z, 45.19Z, 45.20A, 45.20B, 45.31Z, 45.32Z, 45.40Z,47.11A, 47.11B, 47.11C, 47.11D, 47.11E, 47.11F, 47.19A, 47.19B, 47.21Z, 47.22Z, 47.23Z, 47.24Z, 47.25Z, 47.26Z, 47.29Z, 47.30Z, 47.41Z, 47.42Z, 47.43Z, 47.51Z, 47.52A, 47.52B, 47.53Z, 47.54Z, 47.59A, 47.59B, 47.61Z, 47.62Z, 47.63Z, 47.64Z, 47.65Z, 47.71Z, 47.72A, 47.72B, 47.73Z, 47.74Z, 47.75Z, 47.76Z, 47.77Z, 47.78A, 47.78B, 47.78C, 47.79Z, 47.81Z, 47.82Z, 47.89Z, 47.91A, 47.91B, 47.99A, 47.99B,51.10Z, 51.21Z, 51.22Z,53.10Z,55.10Z, 55.20Z, 55.30Z, 55.90Z,56.10A, 56.10B, 56.10C, 56.21Z, 56.29A, 56.29B, 56.30Z,59.11C, 59.14Z, 59.20Z,60.10Z, 60.20A, 60.20B,64.11Z, 64.19Z, 64.20Z, 64.30Z, 64.91Z, 64.92Z, 64.99Z,65.30Z,66.11Z, 66.12Z, 66.19A, 66.19B, 66.21Z, 66.29Z, 66.30Z,68.10Z, 68.20A, 68.20B, 68.31Z, 68.32A, 68.32B,69.10Z, 69.20Z,70.10Z, 70.21Z,71.11Z, 71.20A,75.00Z,77.11A, 77.11B, 77.12Z, 77.21Z, 77.22Z, 77.29Z, 77.31Z, 77.32Z, 77.33Z, 77.34Z, 77.35Z, 77.39Z, 77.40Z,78.10Z, 78.20Z, 78.30Z,80.10Z, 80.20Z, 80.30Z,82.11Z, 82.19Z, 82.20Z, 82.30Z, 82.91Z, 82.99Z,84.11Z, 84.12Z, 84.13Z, 84.21Z, 84.22Z, 84.23Z, 84.24Z, 84.25Z, 84.30A, 84.30B, 84.30C,85.10Z, 85.20Z, 85.31Z, 85.32Z, 85.41Z, 85.42Z, 85.51Z, 85.52Z, 85.53Z, 85.59B, 85.60Z,86.10Z, 86.21Z, 86.22A, 86.22B, 86.22C, 86.23Z, 86.90C, 86.90D, 86.90E, 86.90F,87.10A, 87.10B, 87.10C, 87.20A, 87.20B, 87.30A, 87.30B, 87.90A, 87.90B,88.10A, 88.10B, 88.10C, 88.91A, 88.91B, 88.99A, 88.99B,90.01Z, 90.02Z, 90.03A, 90.03B, 90.04Z,91.01Z, 91.02Z, 91.03Z, 91.04Z,92.00Z,93.11Z, 93.12Z, 93.13Z, 93.19Z, 93.21Z, 93.29Z,94.11Z, 94.12Z, 94.20Z, 94.91Z, 94.92Z, 94.99Z,95.11Z, 95.12Z, 95.21Z, 95.22Z, 95.23Z, 95.24Z, 95.25Z, 95.29Z,96.01A, 96.01B, 96.02A, 96.02B, 96.03Z, 96.04Z, 96.09Z,97.00Z,98.10Z, 98.20Z,99.00Z", # Le code NAF ou code APE, un code d'activité suivant la nomenclature de l'INSEE valide en juin 2026 (cf README)
    "tranche_effectif_salarie": "12,21", # Tranche du nombre de salariés (cf README)
    "nature_juridique" : "1000, 5599, 5699, 5410, 5710, 5499, 6589", # Nature de l'entreprise (cf README)
    "per_page": 25,
    "page": 1  
}
headers = {"accept": "application/json"}

DELAY = 1  # Délais en secondes entre chaque requête sinon ça bloque

all_results = []
seen_sirens = set()

print("DÉBUT DE LA RÉCUPÉRATION")

while True:
    print(f"Page {params['page']}...")

    try:
        r = requests.get(base_url, headers=headers, params=params, timeout=20)
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau : {e}")
        break

    # Vérification HTTP
    if r.status_code != 200:
        print(f"Erreur HTTP {r.status_code}")
        print(r.text[:300])
        break

    # Vérification JSON
    try:
        data = r.json()
    except Exception:
        print("Réponse non JSON")
        print(r.text[:300])
        break

    results = data.get("results", [])

    if not results:
        print("Plus de résultats.")
        break

    # Déduplication SIREN
    new_results = []
    for company in results:
        siren = company.get("siren")
        if siren and siren not in seen_sirens:
            seen_sirens.add(siren)
            new_results.append(company)

    if not new_results:
        print("Aucun nouvel établissement trouvé, arrêt.")
        break

    all_results.extend(new_results)
    params["page"] += 1

    time.sleep(DELAY)

print(f"Total entreprises uniques récupérées : {len(all_results)}")

# Ici on a récupéré les données, maintenant ménage !
df_raw = pd.DataFrame(all_results)

# On explose 'siege'
if "siege" in df_raw.columns:
    df_raw = df_raw.explode("siege").reset_index(drop=True)
    siege_df = json_normalize(
        df_raw["siege"].apply(lambda x: x if isinstance(x, dict) else {})
    ).add_prefix("siege_")
    df_raw = pd.concat([df_raw.drop(columns=["siege"]), siege_df], axis=1)

# On explose 'dirigeants'
if "dirigeants" in df_raw.columns:
    df_raw = df_raw.explode("dirigeants").reset_index(drop=True)
    dirigeants_df = json_normalize(
        df_raw["dirigeants"].apply(lambda x: x if isinstance(x, dict) else {})
    ).add_prefix("dirigeant_")
    df_raw = pd.concat([df_raw.drop(columns=["dirigeants"]), dirigeants_df], axis=1)

# On explose 'matching_etablissements'
if "matching_etablissements" in df_raw.columns:
    df_raw = df_raw.explode("matching_etablissements").reset_index(drop=True)

    etab_df = json_normalize(
        df_raw["matching_etablissements"].apply(
            lambda x: x if isinstance(x, dict) else {}
        )
    ).add_prefix("etab_")

    df_raw = pd.concat(
        [df_raw.drop(columns=["matching_etablissements"]), etab_df],
        axis=1
    )

# On explose 'finances'
if "finances" in df_raw.columns:
    finances_df = json_normalize(df_raw["finances"]).add_prefix("finances_")
    df_raw = pd.concat(
        [df_raw.drop(columns=["finances"]), finances_df],
        axis=1
    )

# On exploser 'complements'
if "complements" in df_raw.columns:
    complements_df = json_normalize(df_raw["complements"]).add_prefix("complements_")
    df_raw = pd.concat(
        [df_raw.drop(columns=["complements"]), complements_df],
        axis=1
    )

# On refiltre au cas où
for col in ["complements_est_association", "complements_est_service_public"]:
    if col not in df_raw.columns:
        df_raw[col] = "FAUX"

df_raw["etab_est_siege"] = (
    df_raw["etab_est_siege"]
    .astype(str)
    .str.strip()
    .str.upper()
)

mask_exclude = (
    (df_raw["complements_est_association"] == "VRAI") |
    (df_raw["complements_est_service_public"] == "VRAI") |
    (df_raw["complements_est_ess"] == "VRAI") |
    (df_raw["complements_est_administration"] == "VRAI") |
    (df_raw["etab_est_siege"] == "FALSE") |
    (df_raw["dirigeant_qualite"] == "Administrateur") |
    (df_raw["dirigeant_qualite"] == "Commissaire aux comptes suppléant") |
    (df_raw["dirigeant_qualite"] == "Liquidateur") |
    (df_raw["dirigeant_qualite"] == "Membre du conseil de surveillance") |
    (df_raw["dirigeant_qualite"] == "Membre du directoire") |
    (df_raw["dirigeant_qualite"] == "Président du conseil de surveillance") |
    (df_raw["dirigeant_qualite"] == "Membre") |
    (df_raw["dirigeant_qualite"] == "Commissaire aux comptes titulaire") |
    (df_raw["dirigeant_type_dirigeant"] == "personne physique")
)
df_raw = df_raw[~mask_exclude].reset_index(drop=True)


# On enlève les doublons (il devrait pas en avoir)
if "siren" in df_raw.columns:
    df_raw = df_raw.drop_duplicates(subset="siren", keep="first")

# Et on exporte
output_file = "entreprises_siren_74_V4.xlsx"
df_raw.to_excel(output_file, index=False)

print(f"Fichier créé : {output_file}")