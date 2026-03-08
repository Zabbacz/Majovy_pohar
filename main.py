import sys
from PyQt6.QtWidgets import QApplication

from config import Config
from database import get_engine, Base
from views.ui.styles import APP_STYLE
from views.windows.main_window import MainWindow


def main():
    # Qt aplikace
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    # konfigurace
    config = Config()

    # databáze
    engine = get_engine()
    Base.metadata.create_all(engine)

    # hlavní okno
    win = MainWindow(config)
    win.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
