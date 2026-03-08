APP_STYLE = """
QWidget {
    font-family: Segoe UI;
    font-size: 13px;
}

QMainWindow {
    background-color: #f4f6f8;
}

QGroupBox {
    border: 1px solid #cfd6dd;
    border-radius: 6px;
    margin-top: 8px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}

QPushButton {
    background-color: #1976d2;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
}

QPushButton:hover {
    background-color: #1565c0;
}

QPushButton:disabled {
    background-color: #9e9e9e;
}

QLineEdit {
    border: 1px solid #cfd6dd;
    border-radius: 4px;
    padding: 4px;
}

QTabWidget::pane {
    border: 1px solid #cfd6dd;
    border-radius: 6px;
}

QTabBar::tab {
    padding: 6px 12px;
}

QTableWidget::item:selected {
    background-color: #ffe082;
    color: black;
}

QTableWidget {
    selection-background-color: #ffe082;
}
"""
