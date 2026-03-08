from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QLineEdit,
)
from PyQt6.QtCore import Qt

from utils.keymap import EnterTableWidget
from views.windows.base_child_window import BaseChildWindow
from services.druzstva_service import DruzstvaService
from config import Config


class DruzstvaWindow(BaseChildWindow):

    HEADERS = ["ID", "Jméno", "kategorie", "Ročník", "Oddíl", "Trenér", "gis_id", "Družstvo"]

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.setWindowTitle("Správa závodníků")
        self.resize(800, 500)

        self.kategorie = DruzstvaService.get_categories()
        self.oddily = DruzstvaService.get_departmens()
        self.treneri = DruzstvaService.get_coaches()

        self._init_ui()
        self._load_data()

    # -----------------------------------------------------

    def _init_ui(self):
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Hledat podle jména…")
        self.search_input.textChanged.connect(self._filter_table)

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
        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addWidget(btn_add)
        layout.addWidget(btn_delete)
        layout.addWidget(btn_save)

    # -----------------------------------------------------

    def _load_data(self):
        self.table.setRowCount(0)
        for r in DruzstvaService.get_all():
            self._add_row(
                zavodnik_id = r.zavodnik_id,
                jmeno=r.jmeno,
                kategorie_id = r.kategorie_id,
                rocnik = r.rocnik,
                oddil_id = r.oddil_id,
                trener_id = r.trener_id,
                gis_id = r.gis_id,
                druzstvo=r.druzstvo,
            )

        self._add_empty_row()

    # -----------------------------------------------------

    def _add_empty_row(self):
        self._add_row()

    # -----------------------------------------------------
    def _add_row(
        self,
        zavodnik_id=None,
        jmeno="",
        kategorie_id=None,
        rocnik="",
        oddil_id=None,
        trener_id=None,
        gis_id="",
        druzstvo="",
    ):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # ID
        item_id = QTableWidgetItem("" if zavodnik_id is None else str(zavodnik_id))
        item_id.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table.setItem(row, 0, item_id)

        # Jméno
        self.table.setItem(row, 1, QTableWidgetItem(jmeno))

        # kategorie (COMBO)
        combo_kategorie = QComboBox()
        combo_kategorie.addItem("—", None)
        for n in self.kategorie:
            combo_kategorie.addItem(n.nazev, n.kategorie_id)
        if kategorie_id is not None:
            index = combo_kategorie.findData(kategorie_id)
            if index >= 0:
                combo_kategorie.setCurrentIndex(index)
        self.table.setCellWidget(row, 2, combo_kategorie)

        # oddil (COMBO)
        combo_oddil = QComboBox()
        combo_oddil.addItem("—", None)
        for n in self.oddily:
            combo_oddil.addItem(n.nazev, n.oddil_id)
        if oddil_id is not None:
            index = combo_oddil.findData(oddil_id)
            if index >= 0:
                combo_oddil.setCurrentIndex(index)
        self.table.setCellWidget(row, 4, combo_oddil)

        # trener (COMBO)
        combo_trener = QComboBox()
        combo_trener.addItem("—", None)
        for n in self.treneri:
            combo_trener.addItem(n.jmeno, n.trener_id)
        if trener_id is not None:
            index = combo_trener.findData(trener_id)
            if index >= 0:
                combo_trener.setCurrentIndex(index)
        self.table.setCellWidget(row, 5, combo_trener)

        self.table.setItem(row, 3, QTableWidgetItem(str(rocnik) or ""))

        self.table.setItem(row, 6, QTableWidgetItem(str(gis_id) or ""))

        self.table.setItem(row, 7, QTableWidgetItem(str(druzstvo) or ""))

    # -----------------------------------------------------

    def _collect_data(self):
        items = []

        for row in range(self.table.rowCount()):
            jmeno_item = self.table.item(row, 1)
            if not jmeno_item or not jmeno_item.text().strip():
                continue

            zavodnik_id = self._get_int(row, 0)

            combo_kategorie = self.table.cellWidget(row, 2)
            kategorie_id = combo_kategorie.currentData()

            rocnik = self._get_int(row, 3)

            combo_oddil = self.table.cellWidget(row, 4)
            oddil_id = combo_oddil.currentData()

            combo_trener = self.table.cellWidget(row, 5)
            trener_id = combo_trener.currentData()

            gis_id = self._get_int(row, 6)

            druzstvo = self._get_int(row, 7)

            items.append({
                "id": zavodnik_id,
                "jmeno": jmeno_item.text().strip(),
                "kategorie_id": kategorie_id,
                "rocnik": rocnik,
                "oddil_id": oddil_id,
                "trener_id": trener_id,
                "gis_id": gis_id,
                "druzstvo":druzstvo,
            })

        return items

    # -----------------------------------------------------

    def _save(self):
        try:
            DruzstvaService.save(self._collect_data())
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
        if not item:
            return None

        text = item.text().strip()
        if not text or text.lower() == "none":
            return None

        return int(text)

    def _delete_row(self):
        row = self.table.currentRow()
        if row < 0:
            return

        id_item = self.table.item(row, 0)
        if not id_item or not id_item.text():
            self.table.removeRow(row)
            return

        zavodnik_id = int(id_item.text())

        if QMessageBox.question(
            self,
            "Potvrzení",
            "Opravdu smazat vybraného rozhodčího?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) != QMessageBox.StandardButton.Yes:
            return

        DruzstvaService.delete(zavodnik_id)
        self.table.removeRow(row)

    def _filter_table(self, text: str):
        text = text.lower().strip()

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)  # sloupec Jméno
            if not item:
                self.table.setRowHidden(row, True)
                continue

            name = item.text().lower()
            self.table.setRowHidden(row, text not in name)
