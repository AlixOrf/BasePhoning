from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QWidget,
    QFrame,
)


class EntrepriseDialog(QDialog):

    def __init__(self, entreprise, parent=None):
        super().__init__(parent)

        self.entreprise = entreprise

        # ======================================================
        # FENÊTRE
        # ======================================================

        self.setWindowTitle(
            f"Fiche entreprise - {self.valeur('nom', 'Entreprise')}"
        )

        self.resize(
            900,
            750
        )

        self.setMinimumSize(
            750,
            600
        )

        # ======================================================
        # STYLE
        # ======================================================

        self.setStyleSheet("""
        
        QDialog {
            background-color: #F4F5F7;
        }

        QLabel {
            background-color: transparent;
        }

        /* ==================================================
           TITRE
           ================================================== */

        #dialogTitle {
            color: #303030;
            font-size: 24px;
            font-weight: 700;
        }

        #dialogSubtitle {
            color: #777777;
            font-size: 10pt;
        }

        /* ==================================================
           CARTES
           ================================================== */

        #sectionCard {
            background-color: #FFFFFF;

            border: 1px solid #E1E3E6;
            border-radius: 9px;
        }

        #sectionTitle {
            color: #303030;

            font-size: 13px;
            font-weight: 700;

            padding-bottom: 6px;

            border-bottom: 2px solid #B51F23;
        }

        /* ==================================================
           LABELS
           ================================================== */

        #fieldLabel {
            color: #777777;

            font-size: 9pt;
            font-weight: 600;
        }

        #fieldValue {
            color: #303030;

            font-size: 10pt;
        }

        #emptyValue {
            color: #AAAAAA;

            font-size: 10pt;
            font-style: italic;
        }

        /* ==================================================
           BOUTON
           ================================================== */

        #closeButton {
            background-color: #B51F23;

            color: white;

            border: none;
            border-radius: 7px;

            padding: 10px 25px;

            font-size: 10pt;
            font-weight: 600;
        }

        #closeButton:hover {
            background-color: #991A1D;
        }

        #closeButton:pressed {
            background-color: #801518;
        }

        /* ==================================================
           SCROLL AREA
           ================================================== */

        QScrollArea {
            background-color: transparent;

            border: none;
        }

        QScrollArea > QWidget > QWidget {
            background-color: #F4F5F7;
        }

        QScrollBar:vertical {
            background-color: #F4F5F7;

            width: 10px;

            margin: 0;
        }

        QScrollBar::handle:vertical {
            background-color: #C7C9CC;

            border-radius: 5px;

            min-height: 35px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #999B9E;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }

        """)

        # ======================================================
        # LAYOUT PRINCIPAL
        # ======================================================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            25,
            30,
            20
        )

        layout.setSpacing(
            18
        )

        # ======================================================
        # EN-TÊTE
        # ======================================================

        titre = QLabel(
            self.valeur(
                "nom",
                "Entreprise"
            )
        )

        titre.setObjectName(
            "dialogTitle"
        )

        titre.setWordWrap(
            True
        )

        layout.addWidget(
            titre
        )

        sous_titre = QLabel(
            f"SIREN : {self.valeur('siren')}"
        )

        sous_titre.setObjectName(
            "dialogSubtitle"
        )

        layout.addWidget(
            sous_titre
        )

        # ======================================================
        # SÉPARATION
        # ======================================================

        ligne = QFrame()

        ligne.setFrameShape(
            QFrame.HLine
        )

        ligne.setStyleSheet(
            "color: #E0E2E5;"
        )

        layout.addWidget(
            ligne
        )

        # ======================================================
        # SCROLL AREA
        # ======================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        # ------------------------------------------------------
        # Contenu scrollable
        # ------------------------------------------------------

        contenu = QWidget()

        contenu_layout = QVBoxLayout(
            contenu
        )

        contenu_layout.setContentsMargins(
            0,
            0,
            8,
            0
        )

        contenu_layout.setSpacing(
            15
        )

        # ======================================================
        # SECTION ENTREPRISE
        # ======================================================

        contenu_layout.addWidget(
            self.creer_section(
                "Entreprise",
                [
                    ("SIREN", "siren"),
                    ("Nom", "nom"),
                    ("Établissements", "établissements"),
                    ("Activité principale", "activite_principale"),
                    ("Catégorie entreprise", "categorie_entreprise"),
                    ("Date de création", "date_creation"),
                    ("État administratif", "etat_administratif"),
                    ("Nature juridique", "nature_juridique"),
                    (
                        "Section activité principale",
                        "section_activite_principale"
                    ),
                    (
                        "Tranche effectif salarié",
                        "tranche_effectif_salarie"
                    ),
                ]
            )
        )

        # ======================================================
        # SECTION DIRIGEANT
        # ======================================================

        contenu_layout.addWidget(
            self.creer_section(
                "Dirigeant",
                [
                    ("Nom", "dirigeant_nom"),
                    ("Prénoms", "dirigeant_prenoms"),
                    (
                        "Année de naissance",
                        "dirigeant_annee_de_naissance"
                    ),
                    (
                        "Date de naissance",
                        "dirigeant_date_de_naissance"
                    ),
                    (
                        "Qualité",
                        "dirigeant_qualite"
                    ),
                    (
                        "Type de dirigeant",
                        "dirigeant_type_dirigeant"
                    ),
                    (
                        "SIREN dirigeant",
                        "dirigeant_siren"
                    ),
                    (
                        "Dénomination dirigeant",
                        "dirigeant_denomination"
                    ),
                ]
            )
        )

        # ======================================================
        # SECTION ÉTABLISSEMENT
        # ======================================================

        contenu_layout.addWidget(
            self.creer_section(
                "Établissement",
                [
                    (
                        "Activité établissement",
                        "etab_activite_principale"
                    ),
                    (
                        "Adresse",
                        "etab_adresse"
                    ),
                    (
                        "Code postal",
                        "etab_code_postal"
                    ),
                    (
                        "Commune",
                        "etab_libelle_commune"
                    ),
                    (
                        "Latitude",
                        "etab_latitude"
                    ),
                    (
                        "Longitude",
                        "etab_longitude"
                    ),
                ]
            )
        )

        # ======================================================
        # SECTION FINANCES
        # ======================================================

        contenu_layout.addWidget(
            self.creer_section(
                "Informations financières",
                [
                    (
                        "Chiffre d'affaires récent",
                        "ca_recent"
                    ),
                    (
                        "Résultat net récent",
                        "resultat_net_recent"
                    ),
                ]
            )
        )

        # ======================================================
        # SECTION PROSPECTION
        # ======================================================

        contenu_layout.addWidget(
            self.creer_section(
                "Prospection",
                [
                    (
                        "Téléphone",
                        "telephone"
                    ),
                    (
                        "Email",
                        "email"
                    ),
                    (
                        "Recherche Google",
                        "recherche_google"
                    ),
                    (
                        "Traité",
                        "traite"
                    ),

                    # ------------------------------
                    # Appels / consultant
                    # ------------------------------


                    (
                        "Consultant",
                        "CONSULTANT"
                    ),


                    (
                        "Numéro consultant",
                        "NUMCONSULTANT"
                    ),


                    (
                        "Total appels",
                        "TOTAL_APPELS"
                    ),


                    (
                        "Date appel",
                        "DATE_APPEL"
                    ),


                    (
                        "Durée",
                        "DUREE"
                    ),


                    (
                        "Accord",
                        "ACCORD"
                    ),


                    (
                        "Désaccord",
                        "DESACCORD"
                    ),


                    (
                        "Échec",
                        "ECHEC"
                    ),


                    (
                        "Opérateur",
                        "OPERATEUR"
                    ),


                    (
                        "Commentaire",
                        "COMMENTAIRE"
                    ),


                    # ------------------------------
                    # R1
                    # ------------------------------


                    (
                        "R1 Retraite",
                        "R1RETRAITE"
                    ),


                    (
                        "R1 CA",
                        "R1CA"
                    ),


                    (
                        "R1 Effectif",
                        "R1EFFECTIF"
                    ),


                    (
                        "R1 Portable",
                        "R1PORTABLE"
                    ),


                    (
                        "R1 Date",
                        "R1DATE"
                    ),


                    (
                        "R1 Heure",
                        "R1HEURE"
                    ),


                    (
                        "R1 Remarques",
                        "R1REMARQUES"
                    ),

                ]
            )
        )

        # ======================================================
        # ESPACE FINAL
        # ======================================================

        contenu_layout.addStretch()

        scroll.setWidget(
            contenu
        )

        layout.addWidget(
            scroll,
            1
        )

        # ======================================================
        # BAS DE FENÊTRE
        # ======================================================

        boutons = QHBoxLayout()

        boutons.addStretch()

        fermer = QPushButton(
            "Fermer"
        )

        fermer.setObjectName(
            "closeButton"
        )

        fermer.setCursor(
            Qt.PointingHandCursor
        )

        fermer.clicked.connect(
            self.accept
        )

        boutons.addWidget(
            fermer
        )

        layout.addLayout(
            boutons
        )

    # ==========================================================
    # RÉCUPÉRER VALEUR
    # ==========================================================

    def valeur(
        self,
        attribut,
        valeur_par_defaut=""
    ):
        """
        Récupère proprement une valeur de l'entreprise.
        """

        valeur = getattr(
            self.entreprise,
            attribut,
            None
        )

        if valeur is None:
            return valeur_par_defaut

        texte = str(
            valeur
        ).strip()

        if texte == "":
            return valeur_par_defaut

        return texte

    # ==========================================================
    # CRÉER UNE SECTION
    # ==========================================================

    def creer_section(
        self,
        titre,
        champs
    ):
        """
        Crée une carte contenant plusieurs informations.
        """

        card = QFrame()

        card.setObjectName(
            "sectionCard"
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            20,
            17,
            20,
            17
        )

        layout.setSpacing(
            10
        )

        # ------------------------------------------------------
        # Titre section
        # ------------------------------------------------------

        label_titre = QLabel(
            titre
        )

        label_titre.setObjectName(
            "sectionTitle"
        )

        layout.addWidget(
            label_titre
        )

        # ------------------------------------------------------
        # Champs
        # ------------------------------------------------------

        for nom_affiche, attribut in champs:

            ligne = QHBoxLayout()

            ligne.setSpacing(
                20
            )

            # ----------------------------------------------
            # Nom du champ
            # ----------------------------------------------

            label = QLabel(
                nom_affiche
            )

            label.setObjectName(
                "fieldLabel"
            )

            label.setFixedWidth(
                210
            )

            label.setAlignment(
                Qt.AlignTop
            )

            ligne.addWidget(
                label
            )

            # ----------------------------------------------
            # Valeur
            # ----------------------------------------------

            valeur = self.valeur(
                attribut
            )

            if valeur == "":

                valeur_label = QLabel(
                    "Non renseigné"
                )

                valeur_label.setObjectName(
                    "emptyValue"
                )

            else:

                valeur_label = QLabel(
                    valeur
                )

                valeur_label.setObjectName(
                    "fieldValue"
                )

            valeur_label.setWordWrap(
                True
            )

            valeur_label.setTextInteractionFlags(
                Qt.TextSelectableByMouse
            )

            ligne.addWidget(
                valeur_label,
                1
            )

            layout.addLayout(
                ligne
            )

        return card