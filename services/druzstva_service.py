from typing import List, Dict

from sqlalchemy.exc import SQLAlchemyError
from database.session import get_session
from database.models.admin_models import Zavodnik
from database.models.admin_models import Kategorie
from database.models.admin_models import Oddil
from database.models.admin_models import Trener

class DruzstvaService:
    """Service pro spravu tabulky zavodnici"""

    @staticmethod
    def get_all() -> list[Zavodnik]:
        session = get_session()
        try:
            return (
                session
                .query(Zavodnik)
                .order_by(Zavodnik.kategorie_id, Zavodnik.oddil_id)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def get_categories() -> list[Kategorie]:
        session = get_session()
        try:
            return (
                session
                .query(Kategorie)
                .order_by(Kategorie.kategorie_id)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def get_departmens() -> list[Oddil]:
        session = get_session()
        try:
            return (
                session
                .query(Oddil)
                .order_by(Oddil.nazev)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def get_coaches() -> list[Trener]:
        session = get_session()
        try:
            return (
                session
                .query(Trener)
                .order_by(Trener.jmeno)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def save(items: List[Dict]) -> None:
        """
        items = [
            {
                "id": 1 | None,
                "kategorie_id": 1,
                "rocnik": 2011,
                "oddil_id": 2,
                "trener_id": 2 | None,
                "Druzstvo": 0,
                "jmeno": "Novák",
                "gis_id":737751 | None
            }
        ]
        """
        session = get_session()
        try:
            for data in items:
                if data["id"] is not None:
                    obj = session.get(Zavodnik, data["id"])
                    if not obj:
                        continue
                else:
                    obj = Zavodnik()
                    session.add(obj)

                obj.kategorie_id = data["kategorie_id"]
                obj.rocnik = data["rocnik"]
                obj.oddil_id = data["oddil_id"]
                obj.trener_id = data["trener_id"]
                obj.druzstvo = data["druzstvo"]
                obj.jmeno = data["jmeno"]
                obj.gis_id = data["gis_id"]

            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete(zavodnik_id: int):
        session = get_session()
        try:
            obj = session.get(Zavodnik, zavodnik_id)
            if obj:
                session.delete(obj)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

