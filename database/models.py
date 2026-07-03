from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from database.database import Base


class Entreprise(Base):
    __tablename__ = "entreprises"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # =========================
    # Informations entreprise
    # =========================

    siren = Column(String(9), unique=True, nullable=False, index=True)

    nom = Column(String)

    activite_principale = Column(String)

    categorie_entreprise = Column(String)

    date_creation = Column(Date)

    etat_administratif = Column(String)

    nature_juridique = Column(String)

    section_activite_principale = Column(String)

    tranche_effectif_salarie = Column(String)

    # =========================
    # Dirigeant
    # =========================

    dirigeant_nom = Column(String)

    dirigeant_prenoms = Column(String)

    dirigeant_annee_de_naissance = Column(Integer)

    dirigeant_date_de_naissance = Column(Date)

    dirigeant_qualite = Column(String)

    dirigeant_type_dirigeant = Column(String)

    dirigeant_siren = Column(String)

    dirigeant_denomination = Column(String)

    # =========================
    # Etablissement
    # =========================

    etab_activite_principale = Column(String)

    etab_adresse = Column(String)

    etab_code_postal = Column(String)

    etab_latitude = Column(Float)

    etab_libelle_commune = Column(String)

    etab_longitude = Column(Float)

    # =========================
    # Finances
    # =========================

    ca_recent = Column(String)

    resultat_net_recent = Column(String)

    # =========================
    # Prospection
    # =========================

    recherche_google = Column(String)

    telephone = Column(String)

    traite = Column(Boolean, default=False)