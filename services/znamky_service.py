from database.session import get_session
from database.models.admin_models import Znamky, Zavodnik
from decimal import Decimal
from typing import Iterable

from database.models.admin_models import Zavodnik

class ZnamkyService:

    @staticmethod
    def get_teams() -> list[int]:
        with get_session() as session:
            rows = session.query(Zavodnik.druzstvo).distinct().order_by(Zavodnik.druzstvo).all()
            return [r[0] for r in rows]

    @staticmethod
    def get_zavodnici(
            druzstvo: int | None = None,
            naradi_id: int | None = None,
    ):
        with get_session() as session:
            q = (
                session
                .query(Zavodnik, Znamky)
                .outerjoin(
                    Znamky,
                    (Znamky.zavodnik_id == Zavodnik.zavodnik_id)
                    & (Znamky.naradi_id == naradi_id)
                )
            )

            if druzstvo is not None:
                q = q.filter(Zavodnik.druzstvo == druzstvo)

            return q.order_by(Zavodnik.zavodnik_id).all()

    @staticmethod
    def save(items: list[dict]):
        with get_session() as session:
            for data in items:
                obj = (
                    session.query(Znamky)
                    .filter_by(
                        zavodnik_id=data["zavodnik_id"],
                        naradi_id=data["naradi_id"],
                    )
                    .first()
                )

                if not obj:
                    obj = Znamky(
                        zavodnik_id=data["zavodnik_id"],
                        naradi_id=data["naradi_id"],
                    )
                    session.add(obj)

                obj.znamka_D = data["znamka_D"]
                obj.pen = data["pen"]
                obj.srazky_E = data["srazky_E"]
                obj.vysledna = data["vysledna"]

            session.commit()

    def compute_srazky_E(values: Iterable[Decimal]) -> Decimal:
        """
        values = [Decimal("0.10"), Decimal("0.25"), ...]
        """
        values = [v for v in values if v is not None]

        if not values or sum(values)==0:
            return Decimal("0")

        values = sorted(values)
        n = len(values)

        if n <= 3:
                return 10-(round(sum(values) / Decimal(n), 3))

        if n == 4:
            middle = values[1:3]
            return 10-(round(sum(middle) / Decimal(2), 3))

        # n >= 5
        mid = n // 2
        middle = values[mid-1:mid+2]
        return 10-(round(sum(middle) / Decimal(3), 3))
