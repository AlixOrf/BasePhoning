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
)

from database.crud import recuperer_toutes_les_entreprises

from ui.table_model import EntrepriseTableModel
from ui.filter_proxy_model import FilterProxyModel
from ui.filter_header import FilterHeader
from datetime import datetime
from ui.export_dialog import ExportDialog
from exports.exportdb import exporter


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Base Entreprises")
        self.resize(1400, 750)

        # ======================
        # Fenêtre principale
        # ======================

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)


        # ======================
        # Recherche globale
        # ======================

        recherche_layout = QHBoxLayout()

        recherche_layout.addWidget(
            QLabel("Recherche :")
        )

        self.recherche = QLineEdit()

        self.recherche.setPlaceholderText(
            "Nom, SIREN, commune..."
        )

        recherche_layout.addWidget(
            self.recherche
        )

        layout.addLayout(
            recherche_layout
        )


        # ======================
        # Modèle données
        # ======================

        self.model = EntrepriseTableModel()


        # ======================
        # Proxy filtres + tri
        # ======================

        self.proxy = FilterProxyModel()

        self.proxy.setSourceModel(
            self.model
        )


        # Recherche globale

        self.recherche.textChanged.connect(
            self.proxy.setGlobalFilter
        )


        # ======================
        # Tableau
        # ======================

        self.table = QTableView()


        # Header Excel

        self.header = FilterHeader(
            self.table
        )

        self.header.set_model(
            self.model
        )

        self.header.proxy = self.proxy


        self.table.setModel(
            self.proxy
        )

        self.table.setHorizontalHeader(
            self.header
        )
        print(type(self.table.horizontalHeader()))
        
        self.header.sectionClicked.connect(
        self.header.open_menu
        )

        # Tri colonnes

        self.table.setSortingEnabled(
            True
        )


        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        header.setStretchLastSection(
            True
        )


        self.table.verticalHeader().setVisible(
            False
        )


        layout.addWidget(
            self.table
        )


        # ======================
        # Boutons
        # ======================

        boutons = QHBoxLayout()


        self.btn_import = QPushButton(
            "Importer"
        )

        self.btn_export = QPushButton(
            "Exporter"
        )


        boutons.addWidget(
            self.btn_import
        )

        boutons.addWidget(
            self.btn_export
        )

        boutons.addStretch()


        layout.addLayout(
            boutons
        )


        # ======================
        # Chargement
        # ======================

        self.charger_entreprises()



    # ======================
    # Chargement données
    # ======================

    def charger_entreprises(self):

        entreprises = recuperer_toutes_les_entreprises()

        self.model.charger(
            entreprises
        )

    def exporter_excel(self):

        nb = self.proxy.rowCount()

        if nb == 0:

            QMessageBox.information(
                self,
                "Export",
                "Aucune entreprise à exporter."
            )

            return

        dialog = ExportDialog(nb, self)

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

        nom = f"{personne}_{datetime.now():%Y-%m-%d}.xlsx"

        fichier, _ = QFileDialog.getSaveFileName(
            self,
            "Exporter",
            nom,
            "Excel (*.xlsx)"
        )

        if not fichier:
            return

        entreprises = []

        for row in range(self.proxy.rowCount()):

            proxy_index = self.proxy.index(row, 0)

            source = self.proxy.mapToSource(proxy_index)

            entreprises.append(
                self.model.get_entreprise(source.row())
            )

        exporter(
            fichier,
            entreprises,
            personne
        )

        self.model.actualiser()

        QMessageBox.information(
            self,
            "Export",
            f"{len(entreprises)} entreprises exportées."
        )