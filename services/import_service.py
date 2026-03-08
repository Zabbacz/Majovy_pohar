import os
import pandas as pd
#from sqlalchemy.exc import SQLAlchemyError

from database.session import get_session
from database.models.admin_models import (
    Kategorie, Trener, Zavodnik, Oddil, Rozhodci
)

class ImportService:

    def import_xls(self, path: str)->dict:
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        xls = pd.ExcelFile(path)
        session = get_session()
        result = {}
        imported = 0
        imported_rozhodci = 0
        try:
            for sheet in xls.sheet_names:
                name = sheet.lower().strip()
                if name == "poznamky":
                    continue

                if name == "rozhodci":
                    imported_rozhodci += self._import_rozhodci_sheet(
                        session=session,
                        xls=xls,
                        sheet_name = sheet
                    )
                else:
                    imported += self._import_kategorie_sheet(
                        session=session,
                        xls=xls,
                        sheet_name=sheet
                    )

            session.commit()
            result['rozhodci'] = imported_rozhodci
            result['zavodnici'] = imported
            return result

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    # -----------------------------------------------------

    def _import_kategorie_sheet(self, session, xls, sheet_name: str) -> int:
        df = xls.parse(sheet_name, skiprows=5)

        # Očekáváme minimálně sloupce B–G
        if df.shape[1] < 7:
            raise ValueError(f"List '{sheet_name}' nemá očekávanou strukturu")

        # Kategorie = název listu
        kategorie = self._get_or_create(
            session,
            Kategorie,
            nazev=sheet_name,
        )

        count = 0

        for _, row in df.iterrows():
            gis_raw = row.iloc[1]   # B
            gis_id = None if pd.isna(gis_raw) else int(gis_raw)
            jmeno = row.iloc[3]     # D
            rocnik = row.iloc[4]    # E
            oddil_nazev = row.iloc[5]   # F
            trener_jmeno = row.iloc[6]  # G

            if pd.isna(jmeno):
                continue  # prázdný řádek

            oddil = self._get_or_create(
                session,
                Oddil,
                nazev=str(oddil_nazev).strip()
            )

            trener = self._get_or_create(
                session,
                Trener,
                jmeno=str(trener_jmeno).strip()
            )

            zavodnik = self._get_or_create_zavodnik(
                session=session,
                kategorie=kategorie,
                oddil=oddil,
                trener=trener,
                jmeno=jmeno,
                rocnik=rocnik,
                gis_id=gis_id,
            )
            count += 1

        return count

    # -----------------------------------------------------

    @staticmethod
    def _get_or_create(session, model, **kwargs):
        obj = session.query(model).filter_by(**kwargs).first()
        if obj:
            return obj

        obj = model(**kwargs)
        session.add(obj)
        session.flush()  #  DŮLEŽITÉ: získání ID bez commit
        return obj

    def _get_or_create_zavodnik(
        self,
        session,
        *,
        kategorie,
        oddil,
        trener,
        jmeno: str,
        rocnik: int,
        gis_id: int | None,
    ):
        q = (
            session.query(Zavodnik)
            .filter(
                Zavodnik.kategorie_id == kategorie.kategorie_id,
                Zavodnik.jmeno == jmeno,
                Zavodnik.rocnik == rocnik,
                Zavodnik.trener_id == trener.trener_id,
                Zavodnik.oddil_id == oddil.oddil_id,
            )
        )

        if gis_id is not None:
            q = q.filter(Zavodnik.gis_id == gis_id)

        obj = q.first()
        if obj:
            return obj

        obj = Zavodnik(
            kategorie_id=kategorie.kategorie_id,
            rocnik=rocnik,
            oddil_id=oddil.oddil_id,
            trener_id=trener.trener_id,
            druzstvo=0,
            jmeno=jmeno,
            gis_id=gis_id,
        )

        session.add(obj)
        session.flush()   #  DŮLEŽITÉ

        return obj

    def _import_rozhodci_sheet(self, session, xls, sheet_name):
        df = xls.parse(sheet_name, skiprows=5)

        count = 0

        for _, row in df.iterrows():
            rozhodci_jmeno = row.iloc[0]   # A
            rozhodci_poznamka = self._clean_cell(row.iloc[1])  # B - pokud neni, chci vkladat NULL
            rozhodci_oddil = self._clean_cell(row.iloc[2])    # C - pokud neni, chci vkladat NULL

            if pd.isna(rozhodci_jmeno):
                continue  # prázdný řádek

            rozhodci = self._get_or_create(
                session,
                Rozhodci,
                jmeno=str(rozhodci_jmeno).strip(),
                poznamka=str(rozhodci_poznamka).strip(),
                oddil=str(rozhodci_oddil).strip(),
            )
            count += 1

        return count

    @staticmethod
    def _clean_cell(value):
        if pd.isna(value):
            return ''
        return str(value).strip()
