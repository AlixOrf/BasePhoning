from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QLabel,
    QTableView,
    QHeaderView,
    QMessageBox,
    QFileDialog,
    QFrame,
)

from database.crud import recuperer_toutes_les_entreprises

from imports.import_excel_app import importer_excel_application

from ui.entreprise_dialog import EntrepriseDialog
from ui.table_model import EntrepriseTableModel
from ui.filter_proxy_model import FilterProxyModel
from ui.filter_header import FilterHeader
from ui.export_dialog import ExportDialog

from exports.exportdb import exporter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ======================================================
        # FENÊTRE
        # ======================================================

        self.setWindowTitle(
            "Action Reprise - Base Entreprises"
        )

        self.resize(
            1500,
            850
        )

        self.setMinimumSize(
            1100,
            650
        )

        # ======================================================
        # STYLE
        # ======================================================

        try:

            with open(
                "ui/style.qss",
                "r",
                encoding="utf-8"
            ) as fichier:

                self.setStyleSheet(
                    fichier.read()
                )

        except FileNotFoundError:

            print(
                "Attention : ui/style.qss introuvable."
            )

        # ======================================================
        # FENÊTRE CENTRALE
        # ======================================================

        central = QWidget()

        central.setObjectName(
            "centralWidget"
        )

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout(
            central
        )

        layout.setContentsMargins(
            25,
            22,
            25,
            22
        )

        layout.setSpacing(
            18
        )

        # ======================================================
        # EN-TÊTE
        # ======================================================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # ------------------------------------------------------
        # Titre
        # ------------------------------------------------------

        titres = QVBoxLayout()

        titres.setSpacing(
            2
        )

        titre = QLabel(
            "Base Entreprises"
        )

        titre.setObjectName(
            "mainTitle"
        )

        sous_titre = QLabel(
            "Gestion et suivi des entreprises"
        )

        sous_titre.setObjectName(
            "subTitle"
        )

        titres.addWidget(
            titre
        )

        titres.addWidget(
            sous_titre
        )

        header_layout.addLayout(
            titres
        )

        header_layout.addStretch()

        # ------------------------------------------------------
        # Compteur
        # ------------------------------------------------------

        self.compteur = QLabel(
            "0 entreprises"
        )

        self.compteur.setObjectName(
            "counter"
        )

        self.compteur.setAlignment(
            Qt.AlignCenter
        )

        header_layout.addWidget(
            self.compteur
        )

        layout.addLayout(
            header_layout
        )

        # ======================================================
        # BARRE DE RECHERCHE
        # ======================================================

        recherche_container = QFrame()

        recherche_container.setObjectName(
            "searchCard"
        )

        recherche_layout = QHBoxLayout(
            recherche_container
        )

        recherche_layout.setContentsMargins(
            16,
            14,
            16,
            14
        )

        recherche_layout.setSpacing(
            12
        )

        label_recherche = QLabel(
            "Recherche"
        )

        label_recherche.setObjectName(
            "searchLabel"
        )

        recherche_layout.addWidget(
            label_recherche
        )

        self.recherche = QLineEdit()

        self.recherche.setObjectName(
            "searchInput"
        )

        self.recherche.setPlaceholderText(
            "Nom, SIREN, commune, téléphone..."
        )

        self.recherche.setClearButtonEnabled(
            True
        )

        recherche_layout.addWidget(
            self.recherche
        )

        layout.addWidget(
            recherche_container
        )

        # ======================================================
        # CONNEXION RECHERCHE
        # ======================================================

        # Le proxy continue de gérer la recherche globale.
        self.recherche.textChanged.connect(
            self.proxy_recherche
        )

        # ======================================================
        # MODÈLE
        # ======================================================

        self.model = EntrepriseTableModel()

        # ======================================================
        # PROXY
        # ======================================================

        self.proxy = FilterProxyModel()

        self.proxy.setSourceModel(
            self.model
        )

        # ======================================================
        # CORRECTION CONNEXION RECHERCHE
        # ======================================================

        self.recherche.textChanged.disconnect(
            self.proxy_recherche
        )

        self.recherche.textChanged.connect(
            self.proxy.setGlobalFilter
        )

        # ======================================================
        # TABLEAU
        # ======================================================

        self.table = QTableView()

        self.table.setObjectName(
            "entrepriseTable"
        )

        self.table.setModel(
            self.proxy
        )

        self.table.setSortingEnabled(
            True
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSelectionBehavior(
            QTableView.SelectRows
        )

        self.table.setSelectionMode(
            QTableView.SingleSelection
        )

        self.table.setShowGrid(
            False
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.verticalHeader().setDefaultSectionSize(
            38
        )

        # ======================================================
        # HEADER PERSONNALISÉ
        # ======================================================

        self.header = FilterHeader(
            self.table
        )

        self.header.set_model(
            self.model
        )

        self.header.proxy = self.proxy

        self.table.setHorizontalHeader(
            self.header
        )

        self.header.sectionClicked.connect(
            self.header.open_menu
        )

        # ======================================================
        # DIMENSIONS HEADER
        # ======================================================

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        header.setStretchLastSection(
            True
        )

        # ======================================================
        # DOUBLE-CLIC
        # ======================================================

        self.table.doubleClicked.connect(
            self.ouvrir_fiche_entreprise
        )

        layout.addWidget(
            self.table,
            1
        )

        # ======================================================
        # BARRE D'ACTIONS
        # ======================================================

        actions_container = QFrame()

        actions_container.setObjectName(
            "actionsCard"
        )

        actions_layout = QHBoxLayout(
            actions_container
        )

        actions_layout.setContentsMargins(
            16,
            12,
            16,
            12
        )

        # ------------------------------------------------------
        # Informations
        # ------------------------------------------------------

        self.info_selection = QLabel(
            "Double-cliquez sur une entreprise pour ouvrir sa fiche"
        )

        self.info_selection.setObjectName(
            "infoText"
        )

        actions_layout.addWidget(
            self.info_selection
        )

        actions_layout.addStretch()

        # ------------------------------------------------------
        # Bouton Importer
        # ------------------------------------------------------

        self.btn_import = QPushButton(
            "Importer"
        )

        self.btn_import.setObjectName(
            "importButton"
        )

        self.btn_import.setMinimumWidth(
            120
        )

        self.btn_import.setMinimumHeight(
            40
        )

        self.btn_import.clicked.connect(
            self.importer_excel
        )

        actions_layout.addWidget(
            self.btn_import
        )

        # ------------------------------------------------------
        # Bouton Exporter
        # ------------------------------------------------------

        self.btn_export = QPushButton(
            "Exporter"
        )

        self.btn_export.setObjectName(
            "exportButton"
        )

        self.btn_export.setMinimumWidth(
            120
        )

        self.btn_export.setMinimumHeight(
            40
        )

        self.btn_export.clicked.connect(
            self.exporter_excel
        )

        actions_layout.addWidget(
            self.btn_export
        )

        layout.addWidget(
            actions_container
        )

        # ======================================================
        # CHARGEMENT INITIAL
        # ======================================================

        self.charger_entreprises()

    # ==========================================================
    # RECHERCHE
    # ==========================================================

    def proxy_recherche(self, texte):
        """
        Méthode intermédiaire pour éviter toute erreur
        pendant l'initialisation de l'interface.
        """

        if hasattr(
            self,
            "proxy"
        ):

            self.proxy.setGlobalFilter(
                texte
            )

    # ==========================================================
    # CHARGEMENT DES ENTREPRISES
    # ==========================================================

    def charger_entreprises(self):

        entreprises = (
            recuperer_toutes_les_entreprises()
        )

        self.model.charger(
            entreprises
        )

        self.actualiser_compteur()

    # ==========================================================
    # COMPTEUR
    # ==========================================================

    def actualiser_compteur(self):

        if not hasattr(
            self,
            "proxy"
        ):
            return

        nombre_total = (
            self.model.rowCount()
        )

        nombre_visible = (
            self.proxy.rowCount()
        )

        if nombre_total == nombre_visible:

            self.compteur.setText(
                f"{nombre_total:,} entreprises".replace(
                    ",",
                    " "
                )
            )

        else:

            self.compteur.setText(
                (
                    f"{nombre_visible:,} visibles "
                    f"/ {nombre_total:,}"
                ).replace(
                    ",",
                    " "
                )
            )

    # ==========================================================
    # OUVRIR FICHE ENTREPRISE
    # ==========================================================

    def ouvrir_fiche_entreprise(
        self,
        proxy_index
    ):

        if not proxy_index.isValid():
            return

        # ------------------------------------------------------
        # Conversion proxy -> modèle original
        # ------------------------------------------------------

        source_index = (
            self.proxy.mapToSource(
                proxy_index
            )
        )

        if not source_index.isValid():
            return

        # ------------------------------------------------------
        # Récupération entreprise
        # ------------------------------------------------------

        entreprise = (
            self.model.get_entreprise(
                source_index.row()
            )
        )

        if entreprise is None:
            return

        # ------------------------------------------------------
        # Ouverture fiche
        # ------------------------------------------------------

        dialog = EntrepriseDialog(
            entreprise,
            self
        )

        dialog.exec()

        # ------------------------------------------------------
        # Actualisation après fermeture
        # ------------------------------------------------------

        self.charger_entreprises()

    # ==========================================================
    # IMPORT EXCEL
    # ==========================================================

    def importer_excel(self):

        # ------------------------------------------------------
        # Sélection fichier
        # ------------------------------------------------------

        fichier, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Importer un fichier Excel",
                "",
                "Fichiers Excel (*.xlsx *.xls)"
            )
        )

        if not fichier:
            return

        # ------------------------------------------------------
        # Désactivation bouton
        # ------------------------------------------------------

        self.btn_import.setEnabled(
            False
        )

        self.btn_import.setText(
            "Import en cours..."
        )

        try:

            # --------------------------------------------------
            # Import
            # --------------------------------------------------

            resultat = (
                importer_excel_application(
                    fichier
                )
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur d'import",
                (
                    "Une erreur est survenue pendant "
                    "l'import du fichier.\n\n"
                    f"{e}"
                )
            )

            return

        finally:

            self.btn_import.setEnabled(
                True
            )

            self.btn_import.setText(
                "Importer"
            )

        # ------------------------------------------------------
        # Actualisation
        # ------------------------------------------------------

        self.charger_entreprises()

        # ------------------------------------------------------
        # Résultat
        # ------------------------------------------------------

        QMessageBox.information(
            self,
            "Import terminé",
            (
                "Import terminé avec succès.\n\n"

                f"Format détecté : "
                f"{resultat['format'].capitalize()}\n\n"

                f"Entreprises ajoutées : "
                f"{resultat['ajoutees']}\n"

                f"Entreprises mises à jour : "
                f"{resultat['mises_a_jour']}\n"

                f"Lignes ignorées : "
                f"{resultat['ignorees']}"
            )
        )

    # ==========================================================
    # EXPORT EXCEL
    # ==========================================================

    def exporter_excel(self):

        nb = self.proxy.rowCount()

        # ------------------------------------------------------
        # Vérification
        # ------------------------------------------------------

        if nb == 0:

            QMessageBox.information(
                self,
                "Export",
                "Aucune entreprise à exporter."
            )

            return

        # ------------------------------------------------------
        # Choix personne
        # ------------------------------------------------------

        dialog = ExportDialog(
            nb,
            self
        )

        if not dialog.exec():
            return

        personne = dialog.get_personne()

        if personne is None:

            QMessageBox.warning(
                self,
                "Export",
                "Veuillez choisir Alain ou Stéphane."
            )

            return

        # ------------------------------------------------------
        # Nom fichier
        # ------------------------------------------------------

        nom = (
            f"{personne}_"
            f"{datetime.now():%Y-%m-%d}.xlsx"
        )

        fichier, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Exporter",
                nom,
                "Excel (*.xlsx)"
            )
        )

        if not fichier:
            return

        # ------------------------------------------------------
        # Récupération entreprises visibles
        # ------------------------------------------------------

        entreprises = []

        for row in range(
            self.proxy.rowCount()
        ):

            proxy_index = (
                self.proxy.index(
                    row,
                    0
                )
            )

            source_index = (
                self.proxy.mapToSource(
                    proxy_index
                )
            )

            if not source_index.isValid():
                continue

            entreprise = (
                self.model.get_entreprise(
                    source_index.row()
                )
            )

            if entreprise is not None:

                entreprises.append(
                    entreprise
                )

        # ------------------------------------------------------
        # Désactivation bouton
        # ------------------------------------------------------

        self.btn_export.setEnabled(
            False
        )

        self.btn_export.setText(
            "Export en cours..."
        )

        try:

            exporter(
                fichier,
                entreprises,
                personne
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Erreur d'export",
                (
                    "Une erreur est survenue pendant "
                    "l'export.\n\n"
                    f"{e}"
                )
            )

            return

        finally:

            self.btn_export.setEnabled(
                True
            )

            self.btn_export.setText(
                "Exporter"
            )

        # ------------------------------------------------------
        # Actualisation
        # ------------------------------------------------------

        self.charger_entreprises()

        # ------------------------------------------------------
        # Confirmation
        # ------------------------------------------------------

        QMessageBox.information(
            self,
            "Export terminé",
            (
                f"{len(entreprises)} "
                "entreprises exportées."
            )
        )