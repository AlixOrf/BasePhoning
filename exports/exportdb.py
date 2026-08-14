import random

import pandas as pd

from database.database import SessionLocal
from database.models import Entreprise


def generer_telephone(e, telephones_utilises):
    """
    Retourne le téléphone de la BDD s'il existe.
    Sinon génère un numéro aléatoire unique de 10 chiffres
    sans aucun 0.
    """

    # Si un téléphone existe déjà dans la BDD,
    # on l'utilise directement.
    if e.telephone:
        return e.telephone

    # Sinon, génération d'un numéro aléatoire
    while True:

        tel = "".join(
            str(random.randint(1, 9))
            for _ in range(10)
        )

        if tel not in telephones_utilises:
            telephones_utilises.add(tel)
            return tel


def exporter(fichier, entreprises, personne):

    # Sécurité : aucune personne sélectionnée
    if not personne:
        raise ValueError(
            "Aucune personne sélectionnée pour l'export."
        )

    personne_lower = personne.lower()

    # ==========================================================
    # MARQUAGE DES ENTREPRISES COMME TRAITÉES
    # ==========================================================

    # "Autre" ne modifie PAS le statut traité
    if personne_lower != "autre":

        session = SessionLocal()

        try:

            for e in entreprises:

                entreprise = session.query(Entreprise).filter_by(
                    siren=e.siren
                ).first()

                if entreprise:
                    entreprise.traite = f"traité par {personne}"

            session.commit()

        finally:
            session.close()

    # ==========================================================
    # EXPORT "AUTRE"
    # ==========================================================

    if personne_lower == "autre":

        data = []

        for e in entreprises:

            data.append({

                "siren": e.siren,
                "nom": e.nom,
                "établissements": e.établissements,
                "activite_principale": e.activite_principale,
                "categorie_entreprise": e.categorie_entreprise,
                "date_creation": e.date_creation,
                "etat_administratif": e.etat_administratif,
                "nature_juridique": e.nature_juridique,
                "section_activite_principale": e.section_activite_principale,
                "tranche_effectif_salarie": e.tranche_effectif_salarie,

                "dirigeant_nom": e.dirigeant_nom,
                "dirigeant_prenoms": e.dirigeant_prenoms,
                "dirigeant_annee_de_naissance": e.dirigeant_annee_de_naissance,
                "dirigeant_date_de_naissance": e.dirigeant_date_de_naissance,
                "dirigeant_qualite": e.dirigeant_qualite,
                "dirigeant_type_dirigeant": e.dirigeant_type_dirigeant,
                "dirigeant_siren": e.dirigeant_siren,
                "dirigeant_denomination": e.dirigeant_denomination,

                "etab_activite_principale": e.etab_activite_principale,
                "etab_adresse": e.etab_adresse,
                "etab_code_postal": e.etab_code_postal,
                "etab_latitude": e.etab_latitude,
                "etab_libelle_commune": e.etab_libelle_commune,
                "etab_longitude": e.etab_longitude,

                "ca_recent": e.ca_recent,
                "resultat_net_recent": e.resultat_net_recent,
                "recherche_google": e.recherche_google,
                "telephone": e.telephone,
                "traite": e.traite,
                "email": e.email

            })

        df = pd.DataFrame(data)

    # ==========================================================
    # EXPORT STEPHANE
    # ==========================================================

    elif personne_lower == "stephane":

        data = []
        telephones_utilises = set()

        for e in entreprises:

            tel = generer_telephone(
                e,
                telephones_utilises
            )

            data.append({

                "CIVIL": "",
                "PRENOM": e.dirigeant_prenoms,
                "NOM": e.dirigeant_nom,
                "FONCTION": e.dirigeant_qualite,
                "AGE": e.dirigeant_annee_de_naissance,
                "SIREN": e.siren,
                "COMPANY": e.nom,
                "ADRESS": e.etab_adresse,
                "CP": e.etab_code_postal,
                "VILLE": e.etab_libelle_commune,

                "EMAIL": "a demander",
                "EMAIL GENERIQUE": "",

                "TEL": tel,
                "MOBILE": "",

                "NAF": e.etab_activite_principale,
                "ACTIVITE": e.activite_principale,
                "EFFECTIF": e.tranche_effectif_salarie,
                "FORME": e.nature_juridique,
                "CREATION": e.date_creation,
                "WEBSITE": "",
                "EMAILBASE": "",
                "CONSULTANT": "",
                "NUMCONSULTANT": "",
                "LIEN GOOGLE": e.recherche_google

            })

        df = pd.DataFrame(data)

    # ==========================================================
    # EXPORT ALAIN
    # ==========================================================

    else:

        data = []
        telephones_utilises = set()

        for e in entreprises:

            tel = generer_telephone(
                e,
                telephones_utilises
            )

            data.append({

                "PRENOM": e.dirigeant_prenoms,
                "NOM": e.dirigeant_nom,
                "FONCTION": e.dirigeant_qualite,
                "AGE": e.dirigeant_annee_de_naissance,
                "SIREN": e.siren,
                "COMPANY": e.nom,
                "ADRESS": e.etab_adresse,
                "CP": e.etab_code_postal,
                "VILLE": e.etab_libelle_commune,

                "EMAIL": "a demander",

                "TEL": tel,
                "NAF": e.etab_activite_principale,
                "ACTIVITE": e.activite_principale,
                "EFFECTIF": e.tranche_effectif_salarie,
                "FORME": e.nature_juridique,
                "CREATION": e.date_creation,
                "CONSULTANT": "",
                "NUMCONSULTANT": "",
                "LIEN GOOGLE": e.recherche_google

            })

        df = pd.DataFrame(data)

    # ==========================================================
    # CRÉATION DU FICHIER EXCEL
    # ==========================================================

    df.to_excel(
        fichier,
        index=False
    )