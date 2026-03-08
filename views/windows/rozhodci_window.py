from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
)
from PyQt6.QtCore import Qt

from utils.keymap import EnterTableWidget
from views.windows.base_child_window import BaseChildWindow
from services.rozhodci_service import RozhodciService
from services.naradi_service import NaradiService
from config import Config


class RozhodciWindow(BaseChildWindow):

    HEADERS = ["ID", "Jméno", "Nářadí", "Typ", "Oddíl", "Poznámka"]

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.setWindowTitle("Správa rozhodčích")
        self.resize(800, 500)

        self.naradi = NaradiService.get_active()

        self._init_ui()
        self._load_data()

    # -----------------------------------------------------

    def _init_ui(self):
        self.table = EnterTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.table.setAlternatingRowColors(True)


        btn_add = QPushButton("Přidat řádek")
        btn_delete = QPushButton("Smazat řádek")
        btn_save = QPushButton("Uložit")

        btn_add.clicked.connect(self._add_empty_row)
        btn_delete.clicked.connect(self._delete_row)
        btn_save.clicked.connect(self._save)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(btn_add)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_save)

    # -----------------------------------------------------

    def _load_data(self):
        self.table.setRowCount(0)

        for r in RozhodciService.get_all():
            self._add_row(
                rozhodci_id=r.rozhodci_id,
                jmeno=r.jmeno,
                naradi_id=r.naradi_id,
                rozhodci_typ=r.rozhodci_typ,
                oddil=r.oddil,
                poznamka=r.poznamka,
            )

        self._add_empty_row()

    # -----------------------------------------------------

    def _add_empty_row(self):
        self._add_row()

    # -----------------------------------------------------

    def _add_row(
        self,
        rozhodci_id=None,
        jmeno="",
        naradi_id=None,
        rozhodci_typ="",
        oddil="",
        poznamka="",
    ):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # ID
        item_id = QTableWidgetItem("" if rozhodci_id is None else str(rozhodci_id))
        item_id.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table.setItem(row, 0, item_id)

        # Jméno
        self.table.setItem(row, 1, QTableWidgetItem(jmeno))

        # Nářadí (COMBO)
        combo_naradi = QComboBox()
        combo_naradi.addItem("—", None)
        for n in self.naradi:
            combo_naradi.addItem(n.naradi, n.naradi_id)

        if naradi_id is not None:
            index = combo_naradi.findData(naradi_id)
            if index >= 0:
                combo_naradi.setCurrentIndex(index)

        self.table.setCellWidget(row, 2, combo_naradi)

        self.table.setItem(row, 3, QTableWidgetItem(rozhodci_typ or ""))

        # Oddíl
        self.table.setItem(row, 4, QTableWidgetItem(oddil or ""))

        # Poznámka
        self.table.setItem(row, 5, QTableWidgetItem(poznamka or ""))

    # -----------------------------------------------------

    def _collect_data(self):
        items = []

        for row in range(self.table.rowCount()):
            jmeno_item = self.table.item(row, 1)
            if not jmeno_item or not jmeno_item.text().strip():
                continue

            rozhodci_id = self._get_int(row, 0)

            combo_naradi = self.table.cellWidget(row, 2)
            naradi_id = combo_naradi.currentData()

            rozhodci_typ = self._get_text(row, 3)

            oddil = self._get_text(row, 4)
            poznamka = self._get_text(row, 5)

            items.append({
                "id": rozhodci_id,
                "jmeno": jmeno_item.text().strip(),
                "naradi_id": naradi_id,
                "rozhodci_typ": rozhodci_typ,
                "oddil": oddil,
                "poznamka": poznamka,
            })

        return items

    # -----------------------------------------------------

    def _save(self):
        try:
            RozhodciService.save(self._collect_data())
            QMessageBox.information(self, "OK", "Změny uloženy")
            self._load_data()
        except Exception as e:
            QMessageBox.critical(self, "Chyba", str(e))

    # -----------------------------------------------------

    def _get_text(self, row, col):
        item = self.table.item(row, col)
        return item.text().strip() if item else None

    def _get_int(self, row, col):
        item = self.table.item(row, col)
        if item and item.text():
            return int(item.text())
        return None

    def _delete_row(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_item = self.table.item(row, 0)
        if not id_item or not id_item.text():
            self.table.removeRow(row)
            return

        rozhodci_id = int(id_item.text())

        if QMessageBox.question(
            self,
            "Potvrzení",
            "Opravdu smazat vybraného rozhodčího?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        RozhodciService.delete(rozhodci_id)
        self.table.removeRow(row)