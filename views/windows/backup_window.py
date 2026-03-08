from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QLabel,
)
from config import Config
from views.windows.base_child_window import BaseChildWindow
from services.backup_service import BackupService


class BackupWindow(BaseChildWindow):

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.service = BackupService

        self.setWindowTitle("Záloha databáze")
        self.resize(600, 220)

        self._init_ui()

    # -------------------------------------------------

    def _init_ui(self):
        layout = QVBoxLayout(self)
        cfg = self.config.data
        path = cfg.get("backup_dir")

        btn_backup = QPushButton("Zálohovat")
        btn_backup.clicked.connect(self._run_backup)

        label_backup =  QLabel(f"Záloha bude provedena do adresáře:\n{path}")

        btn_cancel = QPushButton("Zrušit")
        btn_cancel.clicked.connect(self.close)

        btns = QHBoxLayout()
        btns.addWidget(btn_backup)
        btns.addWidget(btn_cancel)

        labels = QHBoxLayout()
        labels.addWidget(label_backup)

        layout.addLayout(labels)
        layout.addLayout(btns)

    # -------------------------------------------------
    # ACTIONS
    # -------------------------------------------------

    def _run_backup(self):
        try:
            service = BackupService(self.config)
            path = service.backup_database()
            QMessageBox.information(
                self,
                "Záloha hotová",
                f"Databáze byla zazálohována do:\n{path}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Chyba zálohy", str(e))