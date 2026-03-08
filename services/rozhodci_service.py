from typing import List, Dict

from sqlalchemy.exc import SQLAlchemyError
from database.session import get_session
from database.models.admin_models import Rozhodci


class RozhodciService:
    """Service pro spravu tabulky rozhodci"""

    @staticmethod
    def get_all() -> list[Rozhodci]:
        session = get_session()
        try:
            return (
                session
                .query(Rozhodci)
                .order_by(Rozhodci.rozhodci_id)
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
                "jmeno": "Novák",
                "naradi_id": 2 | None,
                "rozhodci_typ": "D",
                "oddil": "TJ",
                "poznamka": "hlavní"
            }
        ]
        """
        session = get_session()
        try:
            for data in items:
                if data["id"] is not None:
                    obj = session.get(Rozhodci, data["id"])
                    if not obj:
                        continue
                else:
                    obj = Rozhodci()
                    session.add(obj)

                obj.jmeno = data["jmeno"]
                obj.naradi_id = data["naradi_id"]
                obj.rozhodci_typ = data["rozhodci_typ"]
                obj.oddil = data["oddil"]
                obj.poznamka = data["poznamka"]

            session.commit()

        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def delete(rozhodci_id: int):
        session = get_session()
        try:
            obj = session.get(Rozhodci, rozhodci_id)
            if obj:
                session.delete(obj)
                session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

