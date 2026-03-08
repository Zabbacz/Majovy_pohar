from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import Qt

from utils.keymap import EnterTableWidget
from views.windows.base_child_window import BaseChildWindow
from services.naradi_service import NaradiService
from config import Config


class NaradiWindow(BaseChildWindow):

    HEADERS = ["ID", "Název", "Aktivní"]

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.setWindowTitle("Správa nářadí")
        self.resize(600, 400)

        self._init_ui()
        self._load_data()

    # ---------------------------------------------------------
    def _init_ui(self):
        self.table = EnterTableWidget()
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.table.setAlternatingRowColors(True)


        btn_add = QPushButton("Přidat řádek")
        btn_save = QPushButton("Uložit změny")
        btn_add.clicked.connect(self._add_row)
        btn_save.clicked.connect(self._save)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(btn_add)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    # ---------------------------------------------------------
    def _load_data(self):
        self.table.setRowCount(0)

        for n in NaradiService.get_all():
            self._add_row(n.naradi_id, n.naradi, n.active)

        self._add_row()  # prázdný řádek

    # ---------------------------------------------------------
    def _add_row(self, naradi_id=None, name="", active=True):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_id = QTableWidgetItem(str(naradi_id) if naradi_id else "")
        item_id.setFlags(Qt.ItemFlag.ItemIsEnabled)
        self.table.setItem(row, 0, item_id)

        self.table.setItem(row, 1, QTableWidgetItem(name))

        chk = QTableWidgetItem()
        chk.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        chk.setCheckState(
            Qt.CheckState.Checked if active else Qt.CheckState.Unchecked
        )
        self.table.setItem(row, 2, chk)

    # ---------------------------------------------------------
    def _collect_data(self):
        items = []

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 1)
            if not name_item:
                continue

            name = name_item.text().strip()
            if not name:
                continue

            id_item = self.table.item(row, 0)
            naradi_id = int(id_item.text()) if id_item and id_item.text() else None

            active = (
                self.table.item(row, 2).checkState()
                == Qt.CheckState.Checked
            )

            items.append({
                "id": naradi_id,
                "name": name,
                "active": active
            })

        return items

    # ---------------------------------------------------------
    def _save(self):
        try:
            data = self._collect_data()
            NaradiService.save(data)

            QMessageBox.information(self, "OK", "Změny uloženy")
            self._load_data()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Chyba",
                f"Chyba při ukládání:\n{e}"
            )
