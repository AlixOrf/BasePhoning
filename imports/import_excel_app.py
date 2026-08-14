import pandas as pd

from database.database import SessionLocal
from database.models import Entreprise


# ==========================================================
# MAPPING DES COLONNES
# ==========================================================

# ----------------------------------------------------------
# EXPORT "AUTRE"
# ----------------------------------------------------------

MAPPING_AUTRE = {
    "siren": "siren",
    "nom": "nom",
    "établissements": "établissements",
    "activite_principale": "activite_principale",
    "categorie_entreprise": "categorie_entreprise",
    "date_creation": "date_creation",
    "etat_administratif": "etat_administratif",
    "nature_juridique": "nature_juridique",
    "section_activite_principale": "section_activite_principale",
    "tranche_effectif_salarie": "tranche_effectif_salarie",

    "dirigeant_nom": "dirigeant_nom",
    "dirigeant_prenoms": "dirigeant_prenoms",
    "dirigeant_annee_de_naissance": "dirigeant_annee_de_naissance",
    "dirigeant_date_de_naissance": "dirigeant_date_de_naissance",
    "dirigeant_qualite": "dirigeant_qualite",
    "dirigeant_type_dirigeant": "dirigeant_type_dirigeant",
    "dirigeant_siren": "dirigeant_siren",
    "dirigeant_denomination": "dirigeant_denomination",

    "etab_activite_principale": "etab_activite_principale",
    "etab_adresse": "etab_adresse",
    "etab_code_postal": "etab_code_postal",
    "etab_latitude": "etab_latitude",
    "etab_libelle_commune": "etab_libelle_commune",
    "etab_longitude": "etab_longitude",

    "ca_recent": "ca_recent",
    "resultat_net_recent": "resultat_net_recent",
    "recherche_google": "recherche_google",
    "telephone": "telephone",
    "traite": "traite",
    "email": "email",
}


# ----------------------------------------------------------
# EXPORT ALAIN
# ----------------------------------------------------------

MAPPING_ALAIN = {
    "SIREN": "siren",
    "PRENOM": "dirigeant_prenoms",
    "NOM": "dirigeant_nom",
    "FONCTION": "dirigeant_qualite",
    "AGE": "dirigeant_annee_de_naissance",

    "COMPANY": "nom",

    "ADRESS": "etab_adresse",
    "CP": "etab_code_postal",
    "VILLE": "etab_libelle_commune",

    "TEL": "telephone",

    "NAF": "etab_activite_principale",
    "ACTIVITE": "activite_principale",
    "EFFECTIF": "tranche_effectif_salarie",
    "FORME": "nature_juridique",
    "CREATION": "date_creation",

    "LIEN GOOGLE": "recherche_google",
}


# ----------------------------------------------------------
# EXPORT STEPHANE
# ----------------------------------------------------------

MAPPING_STEPHANE = {
    "SIREN": "siren",
    "PRENOM": "dirigeant_prenoms",
    "NOM": "dirigeant_nom",
    "FONCTION": "dirigeant_qualite",
    "AGE": "dirigeant_annee_de_naissance",

    "COMPANY": "nom",

    "ADRESS": "etab_adresse",
    "CP": "etab_code_postal",
    "VILLE": "etab_libelle_commune",

    "EMAIL": "email",

    "TEL": "telephone",

    "NAF": "etab_activite_principale",
    "ACTIVITE": "activite_principale",
    "EFFECTIF": "tranche_effectif_salarie",
    "FORME": "nature_juridique",
    "CREATION": "date_creation",

    "LIEN GOOGLE": "recherche_google",
}


# ==========================================================
# OUTILS
# ==========================================================

def valeur_valide(valeur):
    """
    Retourne False si la valeur Excel est vide.
    """

    if valeur is None:
        return False

    try:
        if pd.isna(valeur):
            return False
    except (TypeError, ValueError):
        pass

    if isinstance(valeur, str):

        if not valeur.strip():
            return False

    return True


def nettoyer_valeur(valeur):

    if not valeur_valide(valeur):
        return None

    return valeur


def convertir_siren(valeur):

    if not valeur_valide(valeur):
        return None

    try:

        # Cas Excel :
        # 123456789.0

        if isinstance(valeur, float):

            valeur = int(valeur)

        else:

            texte = str(valeur).strip()

            if texte.endswith(".0"):
                texte = texte[:-2]

            valeur = texte

        siren = str(valeur).strip()

        # Supprime les éventuels espaces
        siren = siren.replace(" ", "")

        # Vérification
        if not siren.isdigit():
            return None

        siren = siren.zfill(9)

        if len(siren) != 9:
            return None

        return siren

    except (ValueError, TypeError):

        return None


def convertir_date(valeur):

    if not valeur_valide(valeur):
        return None

    try:

        return pd.to_datetime(
            valeur
        ).date()

    except Exception:

        return None


def convertir_annee(valeur):

    if not valeur_valide(valeur):
        return None

    try:

        return int(
            float(valeur)
        )

    except (ValueError, TypeError):

        return None


# ==========================================================
# DÉTECTION DU FORMAT
# ==========================================================

def detecter_format(df):

    colonnes = {
        str(colonne).strip()
        for colonne in df.columns
    }

    # --------------------------------------------
    # AUTRE
    # --------------------------------------------

    if "siren" in colonnes:

        return "autre", MAPPING_AUTRE

    # --------------------------------------------
    # ALAIN / STEPHANE
    # --------------------------------------------

    if "SIREN" in colonnes:

        # Stéphane possède notamment EMAIL GENERIQUE
        # et NUMCONSULTANT

        if (
            "EMAIL GENERIQUE" in colonnes
            or "NUMCONSULTANT" in colonnes
        ):

            return "stephane", MAPPING_STEPHANE

        return "alain", MAPPING_ALAIN

    return None, None


# ==========================================================
# CONSTRUCTION DES DONNÉES
# ==========================================================

def construire_donnees(ligne, mapping):

    donnees = {}

    for colonne_excel, colonne_db in mapping.items():

        if colonne_excel not in ligne.index:
            continue

        valeur = ligne[colonne_excel]

        valeur = nettoyer_valeur(
            valeur
        )

        if valeur is not None:

            donnees[colonne_db] = valeur

    # ------------------------------------------------------
    # SIREN
    # ------------------------------------------------------

    if "siren" in donnees:

        donnees["siren"] = convertir_siren(
            donnees["siren"]
        )

    # ------------------------------------------------------
    # DATES
    # ------------------------------------------------------

    if "date_creation" in donnees:

        donnees["date_creation"] = convertir_date(
            donnees["date_creation"]
        )

    if "dirigeant_date_de_naissance" in donnees:

        donnees[
            "dirigeant_date_de_naissance"
        ] = convertir_date(
            donnees["dirigeant_date_de_naissance"]
        )

    # ------------------------------------------------------
    # ANNÉE DE NAISSANCE
    # ------------------------------------------------------

    if "dirigeant_annee_de_naissance" in donnees:

        donnees[
            "dirigeant_annee_de_naissance"
        ] = convertir_annee(
            donnees[
                "dirigeant_annee_de_naissance"
            ]
        )

    # ------------------------------------------------------
    # SUPPRESSION DES VALEURS VIDES
    # ------------------------------------------------------

    donnees = {
        cle: valeur
        for cle, valeur in donnees.items()
        if valeur is not None
    }

    return donnees


# ==========================================================
# IMPORT EXCEL
# ==========================================================

def importer_excel_application(fichier):

    # ------------------------------------------------------
    # Lecture Excel
    # ------------------------------------------------------

    df = pd.read_excel(
        fichier
    )

    # ------------------------------------------------------
    # Détection du format
    # ------------------------------------------------------

    format_excel, mapping = detecter_format(
        df
    )

    if mapping is None:

        raise ValueError(
            "Format Excel non reconnu.\n\n"
            "Le fichier doit provenir d'un export "
            "Alain, Stéphane ou Autre."
        )

    session = SessionLocal()

    ajoutees = 0
    mises_a_jour = 0
    ignorees = 0

    try:

        # --------------------------------------------------
        # Parcours des lignes
        # --------------------------------------------------

        for _, ligne in df.iterrows():

            donnees = construire_donnees(
                ligne,
                mapping
            )

            # --------------------------------------------------
            # Vérification SIREN
            # --------------------------------------------------

            siren = donnees.get(
                "siren"
            )

            if not siren:

                ignorees += 1
                continue

            # --------------------------------------------------
            # Recherche entreprise
            # --------------------------------------------------

            entreprise = (
                session.query(Entreprise)
                .filter(
                    Entreprise.siren == siren
                )
                .first()
            )

            # ==================================================
            # ENTREPRISE EXISTANTE
            # ==================================================

            if entreprise:

                for cle, valeur in donnees.items():

                    # Le SIREN ne doit jamais être modifié
                    if cle == "siren":
                        continue

                    if hasattr(
                        entreprise,
                        cle
                    ):

                        setattr(
                            entreprise,
                            cle,
                            valeur
                        )

                mises_a_jour += 1

            # ==================================================
            # NOUVELLE ENTREPRISE
            # ==================================================

            else:

                session.add(
                    Entreprise(
                        **donnees
                    )
                )

                ajoutees += 1

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        session.commit()

        return {
            "format": format_excel,
            "ajoutees": ajoutees,
            "mises_a_jour": mises_a_jour,
            "ignorees": ignorees,
        }

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()