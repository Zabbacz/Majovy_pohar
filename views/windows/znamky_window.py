from decimal import Decimal, InvalidOperation

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidgetItem, QMessageBox, QComboBox, QSpinBox
)
from PyQt6.QtCore import Qt

from utils.keymap import EnterTableWidget
from views.windows.base_child_window import BaseChildWindow
from services.znamky_service import ZnamkyService
from services.naradi_service import NaradiService
from config import Config


class ZnamkyWindow(BaseChildWindow):

    BASE_HEADERS = ["ID", "Jméno", "D", "PEN"]

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.setWindowTitle("Zadávání známek")
        self.resize(1000, 600)

        self.pocet_E = 3

        self._init_ui()
        self._init_signals()
        self._reload_table()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _init_ui(self):
        layout = QVBoxLayout(self)

        filters = QHBoxLayout()

        self.combo_druzstvo = QComboBox()
        self.combo_druzstvo.addItem("Všechna družstva", None)
        for d in ZnamkyService.get_teams():
            self.combo_druzstvo.addItem(str(d), d)

        self.combo_naradi = QComboBox()
        self.combo_naradi.addItem("— nářadí —", None)
        for n in NaradiService.get_active():
            self.combo_naradi.addItem(n.naradi, n.naradi_id)

        self.spin_E = QSpinBox()
        self.spin_E.setRange(1, 5)
        self.spin_E.setValue(3)

        btn_load = QPushButton("Načíst")
        btn_load.clicked.connect(self._reload_table)

        filters.addWidget(QLabel("Družstvo:"))
        filters.addWidget(self.combo_druzstvo)
        filters.addWidget(QLabel("Nářadí:"))
        filters.addWidget(self.combo_naradi)
        filters.addWidget(QLabel("Počet E:"))
        filters.addWidget(self.spin_E)
        filters.addWidget(btn_load)

        self.table = EnterTableWidget()
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectItems)
        self.table.setAlternatingRowColors(True)

        btn_save = QPushButton("Uložit známky")
        btn_save.clicked.connect(self._save)

        layout.addLayout(filters)
        layout.addWidget(self.table)
        layout.addWidget(btn_save)

    def _init_signals(self):
        self.table.itemChanged.connect(self._on_item_changed)
        self.table.currentCellChanged.connect(self._on_row_leave)

    # ---------------------------------------------------------
    # TABULKA
    # ---------------------------------------------------------

    def _reload_table(self):
        self.pocet_E = self.spin_E.value()

        headers = (
            self.BASE_HEADERS
            + [f"E{i+1}" for i in range(self.pocet_E)]
            + ["Známka E", "Výsledná"]
        )

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(0)
        self.table.setColumnHidden(0, True)

        rows = ZnamkyService.get_zavodnici(
            druzstvo=self.combo_druzstvo.currentData(),
            naradi_id=self.combo_naradi.currentData(),
        )

        for zavodnik, znamky in rows:
            self._add_row_with_data(zavodnik, znamky)

    def _add_row_with_data(self, z, znamky):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self._set_item(row, 0, z.zavodnik_id, enabled=False)
        self._set_item(row, 1, z.jmeno, enabled=False)

        for i in range(self.pocet_E):
            self._set_item(row, 4 + i, "")

        self._set_item(row, 2, znamky.znamka_D if znamky else "")
        self._set_item(row, 3, znamky.pen if znamky else "")

        self._set_item(row, 4 + self.pocet_E,
                       znamky.srazky_E if znamky else "", enabled=False)

        self._set_item(row, 5 + self.pocet_E,
                       znamky.vysledna if znamky else "", enabled=False)

    # ---------------------------------------------------------
    # VÝPOČTY
    # ---------------------------------------------------------

    def _get_decimal(self, row, col) -> Decimal:
        item = self.table.item(row, col)
        if not item or not item.text().strip():
            return Decimal("0")

        try:
            return Decimal(item.text().replace(",", "."))
        except InvalidOperation:
            raise ValueError("Neplatná hodnota")

    def _recalc_row(self, row: int):
        try:
            znamka_D = self._get_decimal(row, 2)
            pen = self._get_decimal(row, 3)

            e_vals = [
                self._get_decimal(row, c)
                for c in range(4, 4 + self.pocet_E)
            ]

            srazky_E = ZnamkyService.compute_srazky_E(e_vals)
            vysledna = znamka_D - pen + srazky_E

            self._set_text_safe(row, 4 + self.pocet_E, str(srazky_E))
            self._set_text_safe(row, 5 + self.pocet_E, str(vysledna))

        except Exception:
            self._set_text_safe(row, 4 + self.pocet_E, "")
            self._set_text_safe(row, 5 + self.pocet_E, "")

    # ---------------------------------------------------------
    # AUTO SAVE
    # ---------------------------------------------------------

    def _on_row_leave(self, row, col, prev_row, prev_col):
        if prev_row < 0 or row == prev_row:
            return

        if self._is_row_complete(prev_row):
            self._save_row(prev_row)

    def _is_row_complete(self, row: int) -> bool:
        try:
            self._get_decimal(row, 2)
            self._get_decimal(row, 3)

            for c in range(4, 4 + self.pocet_E):
                item = self.table.item(row, c)
                if not item or not item.text().strip():
                    return False

            return True
        except Exception:
            return False

    def _save_row(self, row: int):
        naradi_id = self.combo_naradi.currentData()
        if not naradi_id:
            return

        try:
            item = {
                "zavodnik_id": int(self.table.item(row, 0).text()),
                "naradi_id": naradi_id,
                "znamka_D": self._get_decimal(row, 2),
                "pen": self._get_decimal(row, 3),
                "srazky_E": self._get_decimal(row, 4 + self.pocet_E),
                "vysledna": self._get_decimal(row, 5 + self.pocet_E),
            }

            ZnamkyService.save([item])
            self._mark_row_saved(row)

        except Exception:
            pass

    def _mark_row_saved(self, row):
        for c in range(self.table.columnCount()):
            item = self.table.item(row, c)
            if item:
                item.setBackground(Qt.GlobalColor.green)

    # ---------------------------------------------------------
    # MANUAL SAVE
    # ---------------------------------------------------------

    def _save(self):
        for row in range(self.table.rowCount()):
            if self._is_row_complete(row):
                self._save_row(row)

        QMessageBox.information(self, "OK", "Známky uloženy")

    # ---------------------------------------------------------

    def _on_item_changed(self, item: QTableWidgetItem):
        col = item.column()

        if col < 2 or col >= 4 + self.pocet_E:
            return

        try:
            self.table.blockSignals(True)
            self._recalc_row(item.row())
        finally:
            self.table.blockSignals(False)

    def _set_item(self, row, col, value, enabled=True):
        item = QTableWidgetItem(str(value))
        if not enabled:
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table.setItem(row, col, item)

    def _set_text_safe(self, row, col, value):
        item = self.table.item(row, col)
        if item is None:
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(row, col, item)
        item.setText(value)

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def closeEvent(self, event):
        row = self.table.currentRow()
        if row >= 0 and self._is_row_complete(row):
            self._save_row(row)

        super().closeEvent(event)
