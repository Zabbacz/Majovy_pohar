import os
import subprocess
from datetime import datetime

from config import Config


class BackupService:
    """
    Service pro vytvoření SQL dumpu celé databáze.
    """

    def __init__(self, config: Config):
        self.config = config

    # -------------------------------------------------

    def backup_database(self) -> str:
        cfg = self.config.data

        backup_dir = cfg.get("backup_dir")
        if not backup_dir:
            raise ValueError("backup_dir není nastaven v konfiguraci")

        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{cfg['db_name']}_{timestamp}.sql"
        path = os.path.join(backup_dir, filename)

        command = [
            "mysqldump",
            "-h", cfg["db_host"],
            "-P", str(cfg["db_port"]),
            "-u", cfg["db_user"],
            f"--password={cfg['db_password']}",
            "--routines",
            "--triggers",
            "--events",
            cfg["db_name"],
        ]

        try:
            with open(path, "w", encoding="utf-8") as f:
                subprocess.run(
                    command,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True,
                )
        except FileNotFoundError:
            raise RuntimeError("mysqldump nebyl nalezen (není v PATH)")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr.strip())

        return path
