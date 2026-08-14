from collections import Counter
from pathlib import Path
import tempfile
import webbrowser

import folium
from folium.plugins import MarkerCluster

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QSizePolicy,
)

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEBENGINE_DISPONIBLE = True
except ImportError:
    WEBENGINE_DISPONIBLE = False


# ==========================================================
# COULEURS ACTION REPRISE
# ==========================================================

ROUGE = "#B51F24"
BLEU = "#263746"
GRIS = "#6B7280"
FOND = "#F4F5F6"
BLANC = "#FFFFFF"
BORDURE = "#D9DEE3"


# ==========================================================
# DASHBOARD
# ==========================================================

class Dashboard(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.entreprises = []
        self.fichier_carte = None

        self.setStyleSheet(
            f"""
            QWidget {{
                font-family: Arial;
                color: {BLEU};
            }}

            QScrollArea {{
                border: none;
                background: {FOND};
            }}

            QLabel {{
                background: transparent;
            }}

            QPushButton {{
                background: {BLEU};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 9px 18px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background: {ROUGE};
            }}
            """
        )

        self.construire_interface()

    # ======================================================
    # INTERFACE
    # ======================================================

    def construire_interface(self):

        principal = QVBoxLayout(self)
        principal.setContentsMargins(0, 0, 0, 0)

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        header = QFrame()

        header.setStyleSheet(
            f"""
            QFrame {{
                background: {BLANC};
                border-bottom: 1px solid {BORDURE};
            }}
            """
        )

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(
            30, 20, 30, 20
        )

        titre = QLabel("DASHBOARD")

        titre.setStyleSheet(
            f"""
            QLabel {{
                font-size: 28px;
                font-weight: bold;
                color: {BLEU};
            }}
            """
        )

        sous_titre = QLabel(
            "Analyse de la base entreprises"
        )

        sous_titre.setStyleSheet(
            f"""
            QLabel {{
                font-size: 14px;
                color: {GRIS};
            }}
            """
        )

        bloc_titre = QVBoxLayout()

        bloc_titre.addWidget(titre)
        bloc_titre.addWidget(sous_titre)

        header_layout.addLayout(bloc_titre)
        header_layout.addStretch()

        self.btn_retour = QPushButton(
            "← Retour à la base"
        )

        self.btn_retour.clicked.connect(
            self.retour_demande
        )

        header_layout.addWidget(
            self.btn_retour
        )

        principal.addWidget(header)

        # --------------------------------------------------
        # ZONE SCROLLABLE
        # --------------------------------------------------

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        contenu = QWidget()

        self.contenu_layout = QVBoxLayout(
            contenu
        )

        self.contenu_layout.setContentsMargins(
            30, 25, 30, 30
        )

        self.contenu_layout.setSpacing(20)

        scroll.setWidget(contenu)

        principal.addWidget(scroll)

        # --------------------------------------------------
        # CARTES KPI
        # --------------------------------------------------

        self.kpi_layout = QGridLayout()

        self.kpi_layout.setSpacing(15)

        self.contenu_layout.addLayout(
            self.kpi_layout
        )

        # --------------------------------------------------
        # GRAPHIQUES
        # --------------------------------------------------

        self.graphiques_layout = QGridLayout()

        self.graphiques_layout.setSpacing(20)

        self.contenu_layout.addLayout(
            self.graphiques_layout
        )

        # --------------------------------------------------
        # CARTE
        # --------------------------------------------------

        self.carte_frame = QFrame()

        self.carte_frame.setStyleSheet(
            f"""
            QFrame {{
                background: {BLANC};
                border: 1px solid {BORDURE};
                border-radius: 8px;
            }}
            """
        )

        carte_layout = QVBoxLayout(
            self.carte_frame
        )

        titre_carte = QLabel(
            "Localisation des établissements"
        )

        titre_carte.setStyleSheet(
            f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {BLEU};
                padding: 10px;
            }}
            """
        )

        carte_layout.addWidget(
            titre_carte
        )

        if WEBENGINE_DISPONIBLE:

            self.carte = QWebEngineView()

            self.carte.setMinimumHeight(
                550
            )

            carte_layout.addWidget(
                self.carte
            )

        else:

            self.carte = None

            erreur = QLabel(
                "PySide6-WebEngine n'est pas installé.\n\n"
                "Installe-le avec :\n"
                "pip install PySide6-WebEngine"
            )

            erreur.setAlignment(
                Qt.AlignCenter
            )

            erreur.setStyleSheet(
                f"""
                QLabel {{
                    color: {ROUGE};
                    padding: 50px;
                    font-size: 15px;
                }}
                """
            )

            carte_layout.addWidget(
                erreur
            )

        self.contenu_layout.addWidget(
            self.carte_frame
        )

    # ======================================================
    # SIGNAL RETOUR
    # ======================================================

    def retour_demande(self):

        parent = self.parent()

        if parent and hasattr(
            parent,
            "afficher_base"
        ):
            parent.afficher_base()

    # ======================================================
    # RECEVOIR LES ENTREPRISES
    # ======================================================

    def actualiser(self, entreprises):

        self.entreprises = entreprises

        self.construire_dashboard()

    # ======================================================
    # CONSTRUCTION DASHBOARD
    # ======================================================

    def construire_dashboard(self):

        self.vider_layout(
            self.kpi_layout
        )

        self.vider_layout(
            self.graphiques_layout
        )

        nombre = len(
            self.entreprises
        )

        # --------------------------------------------------
        # KPI
        # --------------------------------------------------

        traitees = 0
        non_traitees = 0
        dirigeants = 0
        coordonnees = 0

        for e in self.entreprises:

            if e.traite:
                traitees += 1
            else:
                non_traitees += 1

            if (
                getattr(
                    e,
                    "dirigeant_nom",
                    None
                )
                or
                getattr(
                    e,
                    "dirigeant_prenoms",
                    None
                )
            ):
                dirigeants += 1

            if (
                getattr(
                    e,
                    "etab_latitude",
                    None
                )
                and
                getattr(
                    e,
                    "etab_longitude",
                    None
                )
            ):
                coordonnees += 1

        self.ajouter_kpi(
            0,
            "ENTREPRISES",
            nombre,
            BLEU
        )

        self.ajouter_kpi(
            1,
            "TRAITÉES",
            traitees,
            ROUGE
        )

        self.ajouter_kpi(
            2,
            "NON TRAITÉES",
            non_traitees,
            BLEU
        )

        self.ajouter_kpi(
            3,
            "DIRIGEANTS",
            dirigeants,
            ROUGE
        )

        # --------------------------------------------------
        # GRAPHIQUES
        # --------------------------------------------------

        self.ajouter_graphique(
            "Répartition des traitements",
            self.creer_barres_traite()
        )

        self.ajouter_graphique(
            "Types de dirigeants",
            self.creer_barres_type_dirigeant()
        )

        self.ajouter_graphique(
            "Années de naissance des dirigeants",
            self.creer_barres_naissance()
        )

        self.ajouter_graphique(
            "Top 10 secteurs d'activité",
            self.creer_barres_secteurs()
        )

        self.ajouter_graphique(
            "Répartition des effectifs",
            self.creer_barres_effectifs()
        )

        self.ajouter_graphique(
            "Top 10 formes juridiques",
            self.creer_barres_formes()
        )

        # --------------------------------------------------
        # CARTE
        # --------------------------------------------------

        self.creer_carte()

    # ======================================================
    # KPI
    # ======================================================

    def ajouter_kpi(
        self,
        colonne,
        titre,
        valeur,
        couleur
    ):

        frame = QFrame()

        frame.setMinimumHeight(
            110
        )

        frame.setStyleSheet(
            f"""
            QFrame {{
                background: {BLANC};
                border: 1px solid {BORDURE};
                border-left: 5px solid {couleur};
                border-radius: 8px;
            }}
            """
        )

        layout = QVBoxLayout(frame)

        label_titre = QLabel(
            titre
        )

        label_titre.setStyleSheet(
            f"""
            QLabel {{
                color: {GRIS};
                font-size: 12px;
                font-weight: bold;
            }}
            """
        )

        label_valeur = QLabel(
            f"{valeur:,}"
        )

        label_valeur.setStyleSheet(
            f"""
            QLabel {{
                color: {BLEU};
                font-size: 30px;
                font-weight: bold;
            }}
            """
        )

        layout.addWidget(
            label_titre
        )

        layout.addWidget(
            label_valeur
        )

        self.kpi_layout.addWidget(
            frame,
            0,
            colonne
        )

    # ======================================================
    # CARTE GRAPHIQUE
    # ======================================================

    def ajouter_graphique(
        self,
        titre,
        widget
    ):

        frame = QFrame()

        frame.setMinimumHeight(
            300
        )

        frame.setStyleSheet(
            f"""
            QFrame {{
                background: {BLANC};
                border: 1px solid {BORDURE};
                border-radius: 8px;
            }}
            """
        )

        layout = QVBoxLayout(frame)

        titre_label = QLabel(
            titre
        )

        titre_label.setStyleSheet(
            f"""
            QLabel {{
                color: {BLEU};
                font-size: 17px;
                font-weight: bold;
                padding: 8px;
            }}
            """
        )

        layout.addWidget(
            titre_label
        )

        layout.addWidget(
            widget
        )

        nombre = self.graphiques_layout.count()

        ligne = nombre // 2
        colonne = nombre % 2

        self.graphiques_layout.addWidget(
            frame,
            ligne,
            colonne
        )

    # ======================================================
    # GRAPHIQUE BARRES GENERIQUE
    # ======================================================

    def creer_graphique_barres(
        self,
        valeurs,
        horizontal=False
    ):

        from PySide6.QtWidgets import (
            QProgressBar,
        )

        widget = QWidget()

        layout = QVBoxLayout(widget)

        total = sum(
            valeurs.values()
        )

        if total == 0:

            label = QLabel(
                "Aucune donnée disponible."
            )

            label.setAlignment(
                Qt.AlignCenter
            )

            layout.addWidget(
                label
            )

            return widget

        for nom, nombre in valeurs.items():

            ligne = QHBoxLayout()

            label = QLabel(
                str(nom)
            )

            label.setMinimumWidth(
                130
            )

            label.setWordWrap(
                True
            )

            barre = QProgressBar()

            barre.setRange(
                0,
                total
            )

            barre.setValue(
                nombre
            )

            barre.setFormat(
                f"{nombre:,}  ({nombre / total * 100:.1f} %)"
            )

            barre.setStyleSheet(
                f"""
                QProgressBar {{
                    border: none;
                    background: #E9ECEF;
                    border-radius: 5px;
                    height: 22px;
                    text-align: center;
                }}

                QProgressBar::chunk {{
                    background: {ROUGE};
                    border-radius: 5px;
                }}
                """
            )

            ligne.addWidget(
                label
            )

            ligne.addWidget(
                barre
            )

            layout.addLayout(
                ligne
            )

        return widget

    # ======================================================
    # TRAITE
    # ======================================================

    def creer_barres_traite(self):

        valeurs = Counter()

        for e in self.entreprises:

            statut = e.traite

            if not statut:
                statut = "Non traité"

            valeurs[statut] += 1

        return self.creer_graphique_barres(
            dict(valeurs)
        )

    # ======================================================
    # TYPE DIRIGEANT
    # ======================================================

    def creer_barres_type_dirigeant(self):

        valeurs = Counter()

        for e in self.entreprises:

            valeur = getattr(
                e,
                "dirigeant_type_dirigeant",
                None
            )

            if not valeur:
                valeur = "Inconnu"

            valeurs[str(valeur)] += 1

        valeurs = dict(
            valeurs.most_common(8)
        )

        return self.creer_graphique_barres(
            valeurs
        )

    # ======================================================
    # ANNEE NAISSANCE
    # ======================================================

    def creer_barres_naissance(self):

        valeurs = Counter()

        for e in self.entreprises:

            annee = getattr(
                e,
                "dirigeant_annee_de_naissance",
                None
            )

            if annee:

                try:
                    valeurs[
                        int(annee)
                    ] += 1

                except (
                    ValueError,
                    TypeError
                ):
                    pass

        valeurs = dict(
            sorted(valeurs.items())
        )

        # On limite l'affichage aux années
        # les plus représentées si nécessaire.

        if len(valeurs) > 20:

            valeurs = dict(
                sorted(
                    valeurs.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:20]
            )

            valeurs = dict(
                sorted(
                    valeurs.items()
                )
            )

        return self.creer_graphique_barres(
            valeurs
        )

    # ======================================================
    # SECTEURS
    # ======================================================

    def creer_barres_secteurs(self):

        valeurs = Counter()

        for e in self.entreprises:

            valeur = getattr(
                e,
                "section_activite_principale",
                None
            )

            if not valeur:
                valeur = "Inconnu"

            valeurs[str(valeur)] += 1

        valeurs = dict(
            valeurs.most_common(10)
        )

        return self.creer_graphique_barres(
            valeurs
        )

    # ======================================================
    # EFFECTIFS
    # ======================================================

    def creer_barres_effectifs(self):

        valeurs = Counter()

        for e in self.entreprises:

            valeur = getattr(
                e,
                "tranche_effectif_salarie",
                None
            )

            if not valeur:
                valeur = "Inconnu"

            valeurs[str(valeur)] += 1

        valeurs = dict(
            valeurs.most_common()
        )

        return self.creer_graphique_barres(
            valeurs
        )

    # ======================================================
    # FORMES JURIDIQUES
    # ======================================================

    def creer_barres_formes(self):

        valeurs = Counter()

        for e in self.entreprises:

            valeur = getattr(
                e,
                "nature_juridique",
                None
            )

            if not valeur:
                valeur = "Inconnu"

            valeurs[str(valeur)] += 1

        valeurs = dict(
            valeurs.most_common(10)
        )

        return self.creer_graphique_barres(
            valeurs
        )

    # ======================================================
    # CARTE FOLIUM
    # ======================================================

    def creer_carte(self):

        if not WEBENGINE_DISPONIBLE:
            return

        points = []

        for e in self.entreprises:

            lat = getattr(
                e,
                "etab_latitude",
                None
            )

            lon = getattr(
                e,
                "etab_longitude",
                None
            )

            if lat is None or lon is None:
                continue

            try:

                lat = float(lat)
                lon = float(lon)

            except (
                ValueError,
                TypeError
            ):
                continue

            points.append(
                (lat, lon, e)
            )

        # --------------------------------------------------
        # Centre France
        # --------------------------------------------------

        if points:

            centre_lat = sum(
                p[0] for p in points
            ) / len(points)

            centre_lon = sum(
                p[1] for p in points
            ) / len(points)

        else:

            centre_lat = 46.603354
            centre_lon = 1.888334

        carte = folium.Map(
            location=[
                centre_lat,
                centre_lon
            ],
            zoom_start=6,
            tiles="OpenStreetMap"
        )

        cluster = MarkerCluster()

        cluster.add_to(
            carte
        )

        for lat, lon, e in points:

            nom = (
                getattr(
                    e,
                    "nom",
                    None
                )
                or
                "Entreprise"
            )

            siren = (
                getattr(
                    e,
                    "siren",
                    None
                )
                or
                ""
            )

            commune = (
                getattr(
                    e,
                    "etab_libelle_commune",
                    None
                )
                or
                ""
            )

            adresse = (
                getattr(
                    e,
                    "etab_adresse",
                    None
                )
                or
                ""
            )

            html = f"""
            <div style="
                font-family: Arial;
                min-width: 220px;
            ">
                <h4 style="
                    color: {BLEU};
                    margin-bottom: 5px;
                ">
                    {nom}
                </h4>

                <b>SIREN :</b> {siren}<br>
                <b>Commune :</b> {commune}<br>
                <b>Adresse :</b> {adresse}
            </div>
            """

            folium.Marker(
                location=[
                    lat,
                    lon
                ],
                popup=folium.Popup(
                    html,
                    max_width=350
                ),
                tooltip=nom,
                icon=folium.Icon(
                    color="red",
                    icon="building",
                    prefix="fa"
                )
            ).add_to(
                cluster
            )

        # --------------------------------------------------
        # Sauvegarde HTML temporaire
        # --------------------------------------------------

        fichier = tempfile.NamedTemporaryFile(
            suffix=".html",
            delete=False
        )

        fichier.close()

        carte.save(
            fichier.name
        )

        self.fichier_carte = (
            fichier.name
        )

        self.carte.setUrl(
            f"file:///{fichier.name.replace(chr(92), '/')}"
        )

    # ======================================================
    # VIDER UN LAYOUT
    # ======================================================

    def vider_layout(self, layout):

        while layout.count():

            item = layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

    # ======================================================
    # UPDATE
    # ======================================================

    def closeEvent(self, event):

        if self.fichier_carte:

            try:
                Path(
                    self.fichier_carte
                ).unlink(
                    missing_ok=True
                )

            except Exception:
                pass

        super().closeEvent(
            event
        )