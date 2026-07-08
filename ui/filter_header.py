from PySide6.QtWidgets import (
    QHeaderView,
    QMenu,
    QWidgetAction,
    QListWidget,
    QListWidgetItem
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


    def set_model(self, model):

        self.model_ref = model


    def mousePressEvent(self, event):

        index = self.logicalIndexAt(
            event.position().toPoint()
        )

        if index >= 0:

            self.open_menu(index)

            return

        super().mousePressEvent(event)



    def open_menu(self, column):

        print(
            "OUVERTURE FILTRE COLONNE :",
            column
        )

        if self.model_ref is None:
            return

        if self.proxy is None:
            return


        menu = QMenu(self)


        valeurs = []


        for row in range(
            self.model_ref.rowCount()
        ):

            index = self.model_ref.index(
                row,
                column
            )

            valeur = self.model_ref.data(index)


            if valeur is None or str(valeur).strip() == "":
                valeur = "(Vide)"

            else:
                valeur = str(valeur)


            if valeur not in valeurs:
                valeurs.append(valeur)



        liste = QListWidget()


        # Option Tous

        tous = QListWidgetItem(
            "Tous"
        )

        tous.setCheckState(
            Qt.Checked
        )

        liste.addItem(
            tous
        )


        # Valeurs

        for valeur in sorted(valeurs):

            item = QListWidgetItem(
                valeur
            )

            item.setCheckState(
                Qt.Checked
            )

            liste.addItem(
                item
            )


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


            # Tout sélectionné = pas de filtre

            if len(selection) == len(valeurs):
                selection = []


            print(
                "FILTRE :",
                column,
                selection
            )


            self.proxy.setColumnFilter(
                column,
                selection
            )


        liste.itemChanged.connect(
            appliquer
        )


        action = QWidgetAction(
            menu
        )

        action.setDefaultWidget(
            liste
        )

        menu.addAction(
            action
        )


        # Position sous la colonne cliquée

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


        menu.exec(
            position
        )