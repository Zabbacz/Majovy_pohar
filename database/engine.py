from sqlalchemy import create_engine
from config.config import Config

_engine = None


def get_engine():
    global _engine

    if _engine is None:
        cfg = Config().data

        uri = (
            f"mysql+pymysql://"
            f"{cfg['db_user']}:{cfg['db_password']}@"
            f"{cfg['db_host']}:{cfg['db_port']}/"
            f"{cfg['db_name']}"
        )

        _engine = create_engine(
            uri,
            echo=False,
            future=True,
            pool_pre_ping=True
        )

    return _engine
