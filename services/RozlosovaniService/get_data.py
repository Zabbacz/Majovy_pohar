from database.session import get_session
from database.models import Zavodnik, Oddil
from sqlalchemy.orm import joinedload

class RozlosovaniService:

    @staticmethod
    def get_data() -> list[dict]:
        with get_session() as session:
            rows = (
                session.query(Zavodnik)
                .options(joinedload(Zavodnik.oddil))
                .order_by(Zavodnik.druzstvo, Zavodnik.zavodnik_id)
                .all()
            )

            data: dict[str, list] = {}

            for z in rows:
                druzstvo = f"Družstvo {z.druzstvo}"

                if druzstvo not in data:
                    data[druzstvo] = []

                data[druzstvo].append({
                    "jmeno": z.jmeno,
                    "rocnik": z.rocnik,
                    "oddil": z.oddil.nazev if z.oddil else "",
                })

            return [
                {"druzstvo": name, "zavodnici": zavodnici}
                for name, zavodnici in data.items()
            ]
