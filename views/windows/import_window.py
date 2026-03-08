from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)
from config import Config
from views.windows.base_child_window import BaseChildWindow
from services.import_service import ImportService


class ImportWindow(BaseChildWindow):

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.service = ImportService()
        self.selected_file: str | None = None

        self.setWindowTitle("Import dat")
        self.resize(600, 220)

        self._selected_file: str | None = None
        self._init_ui()

    # -------------------------------------------------

    def _init_ui(self):
        layout = QVBoxLayout(self)

        self.lbl_path = QLabel("Nebyl vybrán žádný soubor")
        layout.addWidget(self.lbl_path)

        btn_select = QPushButton("Vybrat soubor")
        btn_select.clicked.connect(self._select_file)

        btn_import = QPushButton("Importovat")
        btn_import.clicked.connect(self._run_import)

        btn_cancel = QPushButton("Zrušit")
        btn_cancel.clicked.connect(self.close)

        btns = QHBoxLayout()
        btns.addWidget(btn_select)
        btns.addWidget(btn_import)
        btns.addWidget(btn_cancel)

        layout.addLayout(btns)

    # -------------------------------------------------
    # ACTIONS
    # -------------------------------------------------

    def _select_file(self):
        start_dir = self.config.data.get("import_dir", "")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Vyber XLS soubor",
            start_dir,
            "Excel (*.xlsx *.xls)"
        )

        if file_path:
            self._selected_file = file_path
            self.lbl_path.setText(file_path)

    def _run_import(self):
        if not self._selected_file:
            QMessageBox.warning(self, "Chyba", "Vyberte soubor")
            return

        try:
            result = self.service.import_xls(self._selected_file)

            QMessageBox.information(
                self,
                "Import dokončen",
                (
                    "Import proběhl úspěšně\n\n"
                    f"Závodníků: {result.get('zavodnici', 0)}\n"
                    f"Rozhodčích: {result.get('rozhodci', 0)}"
                )
            )
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Chyba importu", str(e))
