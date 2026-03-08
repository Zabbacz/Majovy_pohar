from sqlalchemy import text
from database.session import get_session
from collections import defaultdict


class VysledkyService:

    @staticmethod
    def create_views() -> None:
        # smažeme staré view
        drop_vysledky = """DROP VIEW IF EXISTS v_vysledky"""
        drop_missing = """DROP VIEW IF EXISTS v_chybi_naradi"""

        with get_session() as session:
            session.execute(text(drop_vysledky))
            session.execute(text(drop_missing))
            session.commit()

        # ===============================
        # 1️⃣ HLAVNÍ VÝSLEDKY
        # ===============================

        sql_vysledky = """
                CREATE VIEW v_vysledky AS
                SELECT
                    z.zavodnik_id,
                    z.jmeno,
                    z.rocnik,
                    o.nazev AS oddil,
                    t.jmeno AS trener,
                    k.nazev AS kategorie,
                    n.naradi,
                    n.naradi_id,
                    COALESCE(zn.znamka_D, 0) AS znamka_D,
                    COALESCE(zn.srazky_E, 0) AS znamka_E,
                    COALESCE(zn.pen, 0) AS pen,
                    COALESCE(zn.vysledna, 0) AS vysledna,
                    SUM(COALESCE(zn.vysledna, 0)) OVER (
                        PARTITION BY z.zavodnik_id
                    ) AS celkem,
                    SUM(COALESCE(zn.znamka_D, 0)) OVER (
                        PARTITION BY z.zavodnik_id
                    ) AS d_celkem
                FROM zavodnici z
                JOIN oddily o ON o.oddil_id = z.oddil_id
                JOIN kategorie k ON k.kategorie_id = z.kategorie_id
                JOIN treneri t ON t.trener_id = z.trener_id
                CROSS JOIN naradi n
                LEFT JOIN znamky zn
                ON zn.zavodnik_id = z.zavodnik_id
                AND zn.naradi_id = n.naradi_id
                WHERE n.active = 1
                """

        # ===============================
        # 2️⃣ CHYBĚJÍCÍ NÁŘADÍ
        # ===============================


        sql_missing="""
            CREATE VIEW v_chybi_naradi AS
            SELECT
                z.zavodnik_id,
                z.jmeno,
                n.naradi
            FROM zavodnici z
            JOIN kategorie k
                ON k.kategorie_id = z.kategorie_id
            CROSS JOIN naradi n
            LEFT JOIN znamky zn
                ON zn.zavodnik_id = z.zavodnik_id
                AND zn.naradi_id = n.naradi_id
            WHERE (zn.zavodnik_id IS NULL OR zn.vysledna = 0)
            AND n.active = 1
            AND (
                k.nazev NOT LIKE '%minizaci%'
                OR n.naradi_id NOT IN (2,5)
                )
        """


        with get_session() as session:
            session.execute(text(sql_vysledky))
            session.execute(text(sql_missing))
            session.commit()

    @staticmethod
    def get_missing_naradi() -> list[dict]:

        sql = """
        SELECT jmeno, naradi
        FROM v_chybi_naradi
        ORDER BY jmeno, naradi
        """

        with get_session() as session:
            result = session.execute(text(sql)).fetchall()

        return [
            {
                "jmeno": row[0],
                "naradi": row[1],
            }
            for row in result
        ]

    @staticmethod
    def get_data():
        with get_session() as session:
            rows = session.execute(text("SELECT * FROM v_vysledky")).fetchall()

        # 1️⃣ nářadí jako (id, název), seřazené podle id
        naradi_dict = {
            r.naradi_id: r.naradi
            for r in rows
        }

        naradi_list = sorted(
            naradi_dict.items(),  # [(id, nazev), ...]
            key=lambda x: x[0]
        )

        # 2️⃣ seskupení podle závodníka
        zavodnici_dict = {}

        for r in rows:
            key = r.zavodnik_id

            if key not in zavodnici_dict:
                zavodnici_dict[key] = {
                    "zavodnik_id": r.zavodnik_id,
                    "jmeno": r.jmeno,
                    "rocnik": r.rocnik,
                    "oddil": r.oddil,
                    "trener": r.trener,
                    "kategorie": r.kategorie,
                    "celkem": r.celkem,
                    "d_celkem": r.d_celkem,
                    "naradi": {}
                }

            # klíč už podle naradi_id
            zavodnici_dict[key]["naradi"][r.naradi_id] = {
                "D": r.znamka_D,
                "E": r.znamka_E,
                "Pen": r.pen,
                "Vysl": r.vysledna
            }

        # 3️⃣ seskupení podle kategorií
        kategorie_dict = defaultdict(list)

        for z in zavodnici_dict.values():
            kategorie_dict[z["kategorie"]].append(z)

        # 4️⃣ seřazení v rámci kategorie podle celkem
        for kat in kategorie_dict:
            kategorie_dict[kat] = sorted(
                kategorie_dict[kat],
                key=lambda x: (x["celkem"], -x["d_celkem"]), # pri stejne vysledne znamce vitezi nizsi D
                reverse=True
            )

        return {
            "naradi": naradi_list,  # [(id, nazev), ...]
            "kategorie": kategorie_dict
        }