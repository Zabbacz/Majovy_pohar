from database.session import get_session
from database.models import Zavodnik, Naradi
from sqlalchemy.orm import joinedload


class DruzstvaNaradiService:

    SKIP_RULES = {
        "minizaci": {2, 5}
    }

    @staticmethod
    def get_data() -> list[dict]:

        with get_session() as session:

            naradi_list = (
                session.query(Naradi)
                .filter(Naradi.active == 1)
                .order_by(Naradi.naradi_id)
                .all()
            )

            zavodnici = (
                session.query(Zavodnik)
                .options(joinedload(Zavodnik.kategorie))
                .order_by(Zavodnik.druzstvo, Zavodnik.zavodnik_id)
                .all()
            )

        # -------------------------------------------------
        # seskupení závodníků podle družstva
        # -------------------------------------------------

        druzstva = {}

        for z in zavodnici:

            d = z.druzstvo

            if d not in druzstva:
                druzstva[d] = {
                    "kategorie": z.kategorie.nazev,
                    "zavodnici": []
                }

            druzstva[d]["zavodnici"].append(z.jmeno)

        # -------------------------------------------------
        # vytvoření výsledku
        # -------------------------------------------------

        result = []

        for n in naradi_list:

            druzstva_data = []

            for d, data in druzstva.items():

                kategorie = data["kategorie"].lower()

                skip_ids = next(
                    (ids for key, ids in DruzstvaNaradiService.SKIP_RULES.items() if key in kategorie),
                    set()
                )

                if n.naradi_id in skip_ids:
                    continue

                druzstva_data.append({
                    "druzstvo": d,
                    "kategorie": data["kategorie"],
                    "zavodnici": data["zavodnici"]
                })

            if druzstva_data:
                result.append({
                    "naradi": n.naradi,
                    "naradi_id": n.naradi_id,
                    "druzstva": druzstva_data
                })

        return result
