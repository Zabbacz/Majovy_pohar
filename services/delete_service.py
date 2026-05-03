from sqlalchemy.exc import SQLAlchemyError

from database.session import get_session
from database.models.admin_models import (
    Kategorie, Trener, Zavodnik, Oddil, Rozhodci, Znamky
)

class DeleteService:

    def truncate_tables(self)-> dict[str, int]:
        session = get_session()
        result = {}
        try:
            result["Známky"] = session.query(Znamky).delete()
            result["Závodníci"] = session.query(Zavodnik).delete()
            result["Trenéři"] = session.query(Trener).delete()
            result["Oddíly"] = session.query(Oddil).delete()
            result["Kategorie"] = session.query(Kategorie).delete()
            result["Rozhodčí"] = session.query(Rozhodci).delete()

            session.commit()
            return result

        except SQLAlchemyError:
            session.rollback()
            raise

        finally:
            session.close()

