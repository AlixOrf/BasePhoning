from sqlalchemy import select

from database.database import SessionLocal
from database.models import Entreprise


# =========================
# AJOUTER
# =========================

def ajouter_entreprise(**donnees):
    session = SessionLocal()

    try:
        entreprise = Entreprise(**donnees)
        session.add(entreprise)
        session.commit()
        session.refresh(entreprise)
        return entreprise

    finally:
        session.close()


# =========================
# LIRE
# =========================

def recuperer_toutes_les_entreprises():
    session = SessionLocal()

    try:
        return session.query(Entreprise).all()

    finally:
        session.close()


def chercher_par_siren(siren):
    session = SessionLocal()

    try:
        return (
            session.query(Entreprise)
            .filter(Entreprise.siren == siren)
            .first()
        )

    finally:
        session.close()


def chercher_par_nom(nom):
    session = SessionLocal()

    try:
        return (
            session.query(Entreprise)
            .filter(Entreprise.nom.ilike(f"%{nom}%"))
            .all()
        )

    finally:
        session.close()


# =========================
# EXISTE ?
# =========================

def entreprise_existe(siren):
    return chercher_par_siren(siren) is not None


# =========================
# MODIFIER
# =========================

def modifier_entreprise(siren, **modifications):
    session = SessionLocal()

    try:

        entreprise = (
            session.query(Entreprise)
            .filter(Entreprise.siren == siren)
            .first()
        )

        if entreprise is None:
            return False

        for cle, valeur in modifications.items():

            if hasattr(entreprise, cle):
                setattr(entreprise, cle, valeur)

        session.commit()

        return True

    finally:
        session.close()


# =========================
# SUPPRIMER
# =========================

def supprimer_entreprise(siren):
    session = SessionLocal()

    try:

        entreprise = (
            session.query(Entreprise)
            .filter(Entreprise.siren == siren)
            .first()
        )

        if entreprise is None:
            return False

        session.delete(entreprise)
        session.commit()

        return True

    finally:
        session.close()


# =========================
# TRAITEMENT
# =========================

def marquer_traite(siren):
    return modifier_entreprise(siren, traite=True)


def marquer_non_traite(siren):
    return modifier_entreprise(siren, traite=False)