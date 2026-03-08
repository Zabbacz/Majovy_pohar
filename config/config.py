import json
import os
from datetime import datetime


class Config:

    def __init__(self):
        self.default_path = "config/app_config.json"

        # Výchozí hodnoty
        self.data = {
            "db_host": "localhost",
            "db_port": 3306,
            "db_user": "",
            "db_password": "",
            "db_name": "",
            "backup_dir": "",
            "export_dir": "",
            "import_dir": "",
            "competition_name": "Májový pohár",
            "current_year": datetime.now().year
        }

        self.load()

    def load(self):

        if os.path.exists(self.default_path):
            with open(self.default_path, "r", encoding="utf-8") as f:
                self.data.update(json.load(f))
            return

        self.save()

    def save(self):

        # pokud existuje app_config.json → ukládáme tam
        target = self.default_path

        with open(target, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
