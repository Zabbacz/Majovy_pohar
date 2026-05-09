from PyQt6.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout, QGridLayout, QGroupBox, QMessageBox

from pathlib import Path
from config import Config
from utils.XlsxFormat import format_numeric_cells
from views.windows.config_window import ConfigWindow
from views.windows.naradi_window import NaradiWindow
from views.windows.import_window import ImportWindow
from views.windows.delete_window import DeleteWindow
from views.windows.backup_window import BackupWindow
from views.windows.rozhodci_window import RozhodciWindow
from views.windows.druzstva_window import DruzstvaWindow
from views.windows.znamky_window import ZnamkyWindow
from services.RozlosovaniService import RozlosovaniService
from services.DruzstvaNaradiService import DruzstvaNaradiService
from services.VysledkyService import VysledkyService
from services.export_service import ExportService
from utils.file_utils import open_pdf
from utils.dialogs import show_confirm
from utils.dialogs import show_info

class MainWindow(QMainWindow):

    def __init__(self, config: Config, parent=None):
        super().__init__(parent)

        self.config = config
        self._windows: dict[str, QWidget] = {}

        self.setWindowTitle("Májový pohár – administrace")

        self.resize(1200, 800)

        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        # Použijeme QGridLayout pro maticové uspořádání
        grid_layout = QGridLayout()


        btn_config = QPushButton("Konfigurace")
        btn_config.clicked.connect(self.open_config)

        btn_import = QPushButton("Import startovky z GIS")
        btn_import.clicked.connect(self.open_import)

        btn_export = QPushButton("Export výsledků pro GIS")
        btn_export.clicked.connect(self.get_gis)

        btn_backup = QPushButton("Záloha současné databáze")
        btn_backup.clicked.connect(self.open_backup)

        btn_delete = QPushButton("Smazání současné databáze")
        btn_delete.clicked.connect(self.open_delete)


        btn_naradi = QPushButton("Nářadí")
        btn_naradi.clicked.connect(self.open_naradi)

        btn_rozhodci = QPushButton("Rozhodčí")
        btn_rozhodci.clicked.connect(self.open_rozhodci)

        btn_druzstva = QPushButton("Družstva")
        btn_druzstva.clicked.connect(self.open_druzstva)

        btn_znamky = QPushButton("Známky")
        btn_znamky.clicked.connect(self.open_znamky)

        btn_rozlosovani = QPushButton("Rozlosování")
        btn_rozlosovani.clicked.connect(self.generate_rozlosovani)

        btn_listky = QPushButton("Lístky pro rozhodčí")
        btn_listky.clicked.connect(self.generate_listky)

        btn_vysledky = QPushButton("Výsledky")
        btn_vysledky.clicked.connect(self.generate_vysledky)

        # --- Uspořádání do Mřížky (2x2) ---
        # QGridLayout.addWidget(widget, řádek, sloupec, [rozpětí řádků, rozpětí sloupců])

        # Skupina 1: Nastavení (Řádek 0, Sloupec 0)

        group_config = QGroupBox("Konfigurace / Správa")
        vbox_config = QVBoxLayout(group_config)

        vbox_config.addWidget(btn_config)
        vbox_config.addWidget(btn_backup)
        vbox_config.addWidget(btn_delete)
        vbox_config.addWidget(btn_export)

        grid_layout.addWidget(group_config, 0, 0)

        group_data = QGroupBox("Importy / Exporty")
        vbox_data = QVBoxLayout(group_data)

        vbox_data.addWidget(btn_import)
        vbox_data.addWidget(btn_export)


        grid_layout.addWidget(group_data, 1, 0)

        # Skupina 2: Závodníci / Kategorie (Řádek 0, Sloupec 1)
        # Zde můžete použít vnořený layout, pokud chcete umístit více tlačítek do jedné buňky

        # Vytvoříme GroupBox pro vizuální seskupení a přidáme jej do buňky
        group_zavodnici = QGroupBox("Závodníci / Kategorie / Nářadí")
        vbox_zavodnici = QVBoxLayout(group_zavodnici)
        vbox_zavodnici.addWidget(btn_naradi)
        vbox_zavodnici.addWidget(btn_rozhodci)
        vbox_zavodnici.addWidget(btn_druzstva)
        #        vbox_zavodnici.addWidget(btn_kategorie)
        #        vbox_zavodnici.addWidget(btn_zavodnici)

        grid_layout.addWidget(group_zavodnici, 0, 1)

        # Skupina 3: Závodníci / Kategorie (Řádek 0, Sloupec 1)
        # Zde můžete použít vnořený layout, pokud chcete umístit více tlačítek do jedné buňky

        # Vytvoříme GroupBox pro vizuální seskupení a přidáme jej do buňky
        group_sestavy = QGroupBox("Sestavy pro tisk")
        vbox_sestavy = QVBoxLayout(group_sestavy)
        vbox_sestavy.addWidget(btn_rozlosovani)
        vbox_sestavy.addWidget(btn_listky)
        vbox_sestavy.addWidget(btn_vysledky)
        grid_layout.addWidget(group_sestavy, 1,1)

        # Skupina 4: frontend (Řádek 1, Sloupec 1)
        group_znamky = QGroupBox("Frotend")
        vbox_znamky = QVBoxLayout(group_znamky)
        vbox_znamky.addWidget(btn_znamky)
        grid_layout.addWidget(group_znamky, 2, 0)

        # --- Hlavní Layout okna (Pro zachování addStretch) ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(grid_layout)  # Přidáme mřížku jako celek
        main_layout.addStretch()  # Vytlačí mřížku nahoru

        central.setLayout(main_layout)

        self.setCentralWidget(central)

    # ---------------- ROUTER ----------------

    def _open_window(self, key: str, window_cls):
        if key in self._windows:
            self._windows[key].raise_()
            self._windows[key].activateWindow()
            return

        win = window_cls(key, self.config, self)
        win.closed.connect(self._on_child_closed)
        win.show()

        self._windows[key] = win

    def _on_child_closed(self, key: str):
        self._windows.pop(key, None)

    # ---------------- ACTIONS ----------------

    def open_config(self):
        self._open_window("config", ConfigWindow)

    def open_import(self):
        self._open_window("import", ImportWindow)

    def open_naradi(self):
        self._open_window("naradi", NaradiWindow)

    def open_delete(self):
        self._open_window("delete", DeleteWindow)

    def open_backup(self):
        self._open_window("backup", BackupWindow)

    def open_rozhodci(self):
        self._open_window("rozhodci", RozhodciWindow)

    def open_druzstva(self):
        self._open_window("rozhodci", DruzstvaWindow)

    def open_znamky(self):
        self._open_window("znamky", ZnamkyWindow)

    def generate_rozlosovani(self):
        data = RozlosovaniService.get_data()
        out_dir = self.config.data.get("export_dir")
        out_file = f"{out_dir}/rozlosovani_druzstva.pdf"

        RozlosovaniService.generate_pdf(
            path=out_file,
            data=data,
        )
        open_pdf(out_file)

    def generate_listky(self):
        data = DruzstvaNaradiService.get_data()
        out_dir = self.config.data.get("export_dir")
        out_file = f"{out_dir}/listky.pdf"

        DruzstvaNaradiService.generate_pdf(
            path=out_file,
            data=data
        )
        open_pdf(out_file)

    def generate_vysledky(self):
        VysledkyService.create_views()
        out_dir = self.config.data.get("export_dir")
        out_file = f"{out_dir}/vysledky.pdf"

        missing = VysledkyService.get_missing_naradi()

        if missing:
            text = "\n".join(
                f"{m['jmeno']} – {m['naradi']}"
                for m in missing
            )

            if show_confirm(
                    self,
                    "Chybí známky",
                    f"Tito závodníci nemají známku na všech nářadích:\n\n{text}",
                    f"Stiskni Cancel a doplň známky, nebo Ok pro generování sestavy výsledků"
            ):
                data = VysledkyService.get_data()
                VysledkyService.generate_pdf(
                    year=self.config.data.get("current_year"),
                    competition = self.config.data.get("competition_name"),
                    path=out_file,
                    data=data,
                )
                open_pdf(out_file)
            else:
                self.open_znamky()
                return


    def get_gis(self):
        export_dir = Path(self.config.data.get("import_dir"))
        path = export_dir / "SGM Majovy pohar_startovka.xlsx"

        # Přeformátuj zdrojový soubor před exportem
        format_numeric_cells(str(path))

        result = ExportService.export_to_xlsx(str(path))

        if result["ok"]:
            show_info(self,
                f"Export proběhl v pořádku.\nSoubor:\n{result['file']}"
            )
        else:
            msg = "\n".join(result["errors"])
            show_info(self,
                f"Export dokončen s chybami:\n\n{msg}",
                title="Upozornění"
            )

