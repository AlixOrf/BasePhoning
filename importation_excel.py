import requests
import pandas as pd
from pandas import json_normalize
import time

# Ici les éléments que je filtre pour récupérer mes données
base_url = "https://recherche-entreprises.api.gouv.fr/search"
params = {
    "departement": "74", # Le département, pas compliqué c'est le même que le code postal
    "etat_administratif": "A", # Si l'entreprise est active où non
    "est_association": "false", # Si ce n'est pas une assosiation (revérifier derrière)
    #"activite_principale": "", # Le code NAF ou code APE, un code d'activité suivant la nomenclature de l'INSEE valide en juin 2026 (cf README)
    "tranche_effectif_salarie": "03,11,12,21", # Tranche du nombre de salariés (cf README)
    "categorie_entreprise" :"PME, ETI", # PME, ETI ou GE
    #"nature_juridique" : "", # Nature de l'entreprise (cf README)
    #"section_activite_principale" : #Cf README
    "date_naissance_personne_min" : "1954-01-01",
    "date_naissance_personne_max" : "1972-01-01",
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

# On refiltre assos & service public au cas où
for col in ["complements_est_association", "complements_est_service_public"]:
    if col not in df_raw.columns:
        df_raw[col] = "FAUX"

mask_exclude = (
    (df_raw["complements_est_association"] == "VRAI") |
    (df_raw["complements_est_service_public"] == "VRAI")
)
df_raw = df_raw[~mask_exclude].reset_index(drop=True)

# On enlève les colonnes inutiles
cols_to_drop = [
    "sigle","caractere_employeur","annee_categorie_entreprise","date_fermeture",
    "date_mise_a_jour","date_mise_a_jour_insee","date_mise_a_jour_rne","etat_administratif",
    "statut_diffusion","etab_date_fermeture","etab_etat_administratif","etab_liste_id_organisme_formation",
    "etab_liste_rge","etab_liste_uai","etab_region","etab_siret","etab_statut_diffusion_etablissement",
    "complements_collectivite_territoriale","complements_convention_collective_renseignee","complements_liste_idcc",
    "complements_liste_finess_juridique","complements_egapro_renseignee","complements_est_achats_responsables",
    "complements_est_alim_confiance","complements_est_bio","complements_est_entrepreneur_individuel",
    "complements_liste_id_organisme_formation","complements_identifiant_association",
    "complements_statut_entrepreneur_spectacle","complements_type_siae",
    "complements_collectivite_territoriale.code","complements_collectivite_territorialaire.code_insee",
    "complements_collectivite_territoriale.elus","complements_collectivite_territoriale.niveau"
]

df_raw = df_raw.drop(columns=[c for c in cols_to_drop if c in df_raw.columns], errors="ignore")

# On enlève les doublons (il devrait pas en avoir)
if "siren" in df_raw.columns:
    df_raw = df_raw.drop_duplicates(subset="siren", keep="first")

# Et on exporte
output_file = "entreprises_siren_74_V1.xlsx"
df_raw.to_excel(output_file, index=False)

print(f"Fichier créé : {output_file}")