from PySide6.QtWidgets import (
    QHeaderView,
    QMenu,
    QWidgetAction,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout
)

from PySide6.QtCore import Qt


class FilterHeader(QHeaderView):

    def __init__(self, parent=None):

        super().__init__(
            Qt.Horizontal,
            parent
        )

        self.model_ref = None
        self.proxy = None

        # mémorisation des filtres
        self.checked_values = {}

    # ==========================================================
    # MODÈLE
    # ==========================================================

    def set_model(self, model):

        self.model_ref = model

    # ==========================================================
    # CLIC SUR LE HEADER
    # ==========================================================

    def mousePressEvent(self, event):

        index = self.logicalIndexAt(
            event.position().toPoint()
        )

        if index >= 0:
            self.open_menu(index)
            return

        super().mousePressEvent(event)

    # ==========================================================
    # MENU FILTRE
    # ==========================================================

    def open_menu(self, column):

        if self.model_ref is None:
            return

        if self.proxy is None:
            return

        menu = QMenu(self)

        # ======================================================
        # STYLE DU MENU
        # ======================================================

        menu.setObjectName(
            "filterMenu"
        )

        valeurs = []

        # ======================================================
        # RÉCUPÉRATION DES VALEURS
        # ======================================================

        for row in range(
            self.model_ref.rowCount()
        ):

            index = self.model_ref.index(
                row,
                column
            )

            valeur = self.model_ref.data(
                index
            )

            if valeur is None or str(valeur).strip() == "":
                valeur = "(Vide)"

            else:
                valeur = str(valeur)

            if valeur not in valeurs:
                valeurs.append(valeur)

        valeurs.sort()

        # ======================================================
        # WIDGET PRINCIPAL
        # ======================================================

        widget = QWidget()

        widget.setObjectName(
            "filterWidget"
        )

        layout = QVBoxLayout(
            widget
        )

        layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout.setSpacing(
            8
        )

        # ======================================================
        # LISTE
        # ======================================================

        liste = QListWidget()

        liste.setObjectName(
            "filterList"
        )

        layout.addWidget(
            liste
        )

        # ======================================================
        # TOUS
        # ======================================================

        tous = QListWidgetItem(
            "Tous"
        )

        tous.setFlags(
            tous.flags() |
            Qt.ItemIsUserCheckable
        )

        tous.setCheckState(
            Qt.Checked
        )

        liste.addItem(
            tous
        )

        # ======================================================
        # VALEURS
        # ======================================================

        anciennes_valeurs = (
            self.checked_values.get(
                column,
                None
            )
        )

        for valeur in valeurs:

            item = QListWidgetItem(
                valeur
            )

            item.setFlags(
                item.flags() |
                Qt.ItemIsUserCheckable
            )

            if anciennes_valeurs is None:

                item.setCheckState(
                    Qt.Checked
                )

            else:

                if valeur in anciennes_valeurs:

                    item.setCheckState(
                        Qt.Checked
                    )

                else:

                    item.setCheckState(
                        Qt.Unchecked
                    )

            liste.addItem(
                item
            )

        # ======================================================
        # GESTION "TOUS"
        # ======================================================

        def changer_tous(item):

            if item != tous:
                return

            etat = tous.checkState()

            liste.blockSignals(
                True
            )

            for i in range(
                1,
                liste.count()
            ):

                liste.item(i).setCheckState(
                    etat
                )

            liste.blockSignals(
                False
            )

        liste.itemChanged.connect(
            changer_tous
        )

        # ======================================================
        # BOUTONS
        # ======================================================

        boutons = QHBoxLayout()

        boutons.setSpacing(
            8
        )

        ok = QPushButton(
            "OK"
        )

        ok.setObjectName(
            "filterApplyButton"
        )

        annuler = QPushButton(
            "Annuler"
        )

        annuler.setObjectName(
            "filterCancelButton"
        )

        boutons.addWidget(
            ok
        )

        boutons.addWidget(
            annuler
        )

        layout.addLayout(
            boutons
        )

        # ======================================================
        # ACTION
        # ======================================================

        action = QWidgetAction(
            menu
        )

        action.setDefaultWidget(
            widget
        )

        menu.addAction(
            action
        )

        # ======================================================
        # OK
        # ======================================================

        def appliquer():

            selection = []

            for i in range(
                1,
                liste.count()
            ):

                item = liste.item(i)

                if item.checkState() == Qt.Checked:

                    selection.append(
                        item.text()
                    )

            # sauvegarde état

            self.checked_values[column] = selection

            # applique filtre

            self.proxy.setColumnFilter(
                column,
                selection
            )

            menu.close()

        ok.clicked.connect(
            appliquer
        )

        # ======================================================
        # ANNULER
        # ======================================================

        annuler.clicked.connect(
            menu.close
        )

        # ======================================================
        # POSITION
        # ======================================================

        x = self.sectionViewportPosition(
            column
        )

        y = self.height()

        position = self.viewport().mapToGlobal(
            self.viewport().rect().topLeft()
        )

        position.setX(
            position.x() + x
        )

        position.setY(
            position.y() + y
        )

        # ======================================================
        # AFFICHAGE
        # ======================================================

        menu.exec(
            position
        )