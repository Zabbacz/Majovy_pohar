from typing import List, Dict

from sqlalchemy.exc import SQLAlchemyError

from database.session import get_session
from database.models.admin_models import Naradi


class NaradiService:
    """
    Service layer pro práci s tabulkou naradi
    """

    @staticmethod
    def get_all() -> list[Naradi]:
        with get_session() as session:
            return (
                session
                .query(Naradi)
                .order_by(Naradi.naradi_id)
                .all()
            )

    @staticmethod
    def get_active() -> list[Naradi]:
        session = get_session()
        try:
            return (
                session
                .query(Naradi)
                .filter(Naradi.active == 1)
                .order_by(Naradi.naradi_id)
                .all()
            )
        finally:
            session.close()

    @staticmethod
    def save(items: List[Dict]):
        """
        items = [
            {"id": 1, "name": "Hrazda", "active": True},
            {"id": None, "name": "Kruhy", "active": False},
        ]
        """
        with get_session() as session:
            try:
                for data in items:
                    if data.get("id"):
                        obj = session.get(Naradi, data["id"])
                        if not obj:
                            continue
                        obj.naradi = data["name"]
                        obj.active = data["active"]
                    else:
                        session.add(
                            Naradi(
                                naradi=data["name"],
                                active=data["active"]
                            )
                        )

                session.commit()
            except SQLAlchemyError:
                session.rollback()
                raise
