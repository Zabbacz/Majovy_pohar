from PyQt6.QtWidgets import (
    QWidget, QFileDialog, QLineEdit, QPushButton, QTabWidget,
    QVBoxLayout, QFormLayout, QMessageBox, QHBoxLayout
)

import mysql.connector


from views.windows.base_child_window import BaseChildWindow
from config import Config


class ConfigWindow(BaseChildWindow):

    def __init__(self, key: str, config: Config, parent=None):
        super().__init__(key, config, parent)

        self.setWindowTitle("Nastavení aplikace")
        self.resize(600, 400)

        self._init_ui()

        self.load_values_into_form()

    def _init_ui(self):
        self.tabs = QTabWidget()

        # -----------------------------------------------------------
        # TAB: Databáze
        # -----------------------------------------------------------
        self.db_tab = QWidget()
        db_layout = QFormLayout()

        self.db_host_input = QLineEdit()
        self.db_port_input = QLineEdit()
        self.db_user_input = QLineEdit()
        self.db_pass_input = QLineEdit()
        self.db_name_input = QLineEdit()

        self.db_pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        db_layout.addRow("Host:", self.db_host_input)
        db_layout.addRow("Port:", self.db_port_input)
        db_layout.addRow("Uživatel:", self.db_user_input)
        db_layout.addRow("Heslo:", self.db_pass_input)
        db_layout.addRow("Databáze:", self.db_name_input)

        self.db_tab.setLayout(db_layout)

        # -----------------------------------------------------------
        # TAB: Cesty / rok
        # -----------------------------------------------------------
        self.path_tab = QWidget()
        path_layout = QFormLayout()

        self.backup_dir_input = QLineEdit()
        self.export_dir_input = QLineEdit()
        self.import_dir_input = QLineEdit()
        self.year_input = QLineEdit()
        self.competition_input = QLineEdit()

        # --------------- řádek ZÁLOHY ----------------
        row_backup = QHBoxLayout()
        btn_backup = QPushButton("Vybrat…")
        btn_backup.clicked.connect(self.select_backup_path)
        row_backup.addWidget(self.backup_dir_input)
        row_backup.addWidget(btn_backup)

        backup_widget = QWidget()
        backup_widget.setLayout(row_backup)
        path_layout.addRow("Zálohy:", backup_widget)

        # --------------- řádek EXPORTY ----------------
        row_export = QHBoxLayout()
        btn_export = QPushButton("Vybrat…")
        btn_export.clicked.connect(self.select_export_path)
        row_export.addWidget(self.export_dir_input)
        row_export.addWidget(btn_export)

        export_widget = QWidget()
        export_widget.setLayout(row_export)
        path_layout.addRow("Exporty:", export_widget)

        # --------------- řádek IMPORTY ----------------
        row_import = QHBoxLayout()
        btn_import = QPushButton("Vybrat…")
        btn_import.clicked.connect(self.select_import_path)
        row_import.addWidget(self.import_dir_input)
        row_import.addWidget(btn_import)

        import_widget = QWidget()
        import_widget.setLayout(row_import)
        path_layout.addRow("Importy:", import_widget)

        # Rok
        path_layout.addRow("Aktuální rok:", self.year_input)

        # Nazev zavodu
        path_layout.addRow("název závodu:", self.competition_input)

        self.path_tab.setLayout(path_layout)

        # Tabs
        self.tabs.addTab(self.db_tab, "Databáze")
        self.tabs.addTab(self.path_tab, "Cesty / Rok")

        # -----------------------------------------------------------
        # BUTTONS
        # -----------------------------------------------------------
        self.save_button = QPushButton("Uložit")
        self.save_button.clicked.connect(self.save_values_from_form)

        self.test_button = QPushButton("Otestovat připojení")
        self.test_button.clicked.connect(self.test_connection)

        # -----------------------------------------------------------
        # MAIN LAYOUT
        # -----------------------------------------------------------
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.save_button)
        main_layout.addWidget(self.test_button)
        self.setLayout(main_layout)

    # ===============================================================
    # LOAD VALUES
    # ===============================================================
    def load_values_into_form(self):
        self.db_host_input.setText(self.config.data.get("db_host", ""))
        self.db_port_input.setText(str(self.config.data.get("db_port", "")))
        self.db_user_input.setText(self.config.data.get("db_user", ""))
        self.db_pass_input.setText(self.config.data.get("db_password", ""))
        self.db_name_input.setText(self.config.data.get("db_name", ""))

        self.backup_dir_input.setText(self.config.data.get("backup_dir", ""))
        self.export_dir_input.setText(self.config.data.get("export_dir", ""))
        self.import_dir_input.setText(self.config.data.get("import_dir", ""))
        self.year_input.setText(str(self.config.data.get("current_year", "")))
        self.competition_input.setText(self.config.data.get("competition_name", ""))

    # ===============================================================
    # SAVE
    # ===============================================================
    def save_values_from_form(self):
        self.config.data["db_host"] = self.db_host_input.text()
        self.config.data["db_port"] = int(self.db_port_input.text())
        self.config.data["db_user"] = self.db_user_input.text()
        self.config.data["db_password"] = self.db_pass_input.text()
        self.config.data["db_name"] = self.db_name_input.text()

        self.config.data["backup_dir"] = self.backup_dir_input.text()
        self.config.data["export_dir"] = self.export_dir_input.text()
        self.config.data["import_dir"] = self.import_dir_input.text()
        self.config.data["current_year"] = int(self.year_input.text())
        self.config.data["competiton_name"] = self.competition_input.text()

        self.config.save()
        self._popup("Uloženo.")

    # ===============================================================
    # TEST DB CONNECTION
    # ===============================================================
    def test_connection(self):
        try:
            mysql.connector.connect(
                host=self.db_host_input.text(),
                port=self.db_port_input.text(),
                user=self.db_user_input.text(),
                password=self.db_pass_input.text(),
                database=self.db_name_input.text(),
                connection_timeout=3
            )
            self._popup("Připojení je funkční.")
        except Exception as e:
            self._popup(f"Chyba připojení: {e}")

    # ===============================================================
    # POPUP
    # ===============================================================
    def _popup(self, msg: str):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Informace")
        dlg.setText(msg)
        dlg.exec()

    # ===============================================================
    # SELECT PATHS
    # ===============================================================
    def select_backup_path(self):
        path = QFileDialog.getExistingDirectory(self, "Vyberte složku pro zálohy")
        if path:
            self.backup_dir_input.setText(path)

    def select_export_path(self):
        path = QFileDialog.getExistingDirectory(self, "Vyberte složku pro exporty")
        if path:
            self.export_dir_input.setText(path)

    def select_import_path(self):
        path = QFileDialog.getExistingDirectory(self, "Vyberte složku pro importy")
        if path:
            self.import_dir_input.setText(path)
