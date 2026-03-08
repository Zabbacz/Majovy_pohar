from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, CHAR, LargeBinary, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import YEAR

from database.models.base import Base


#---------- tables ----------#

class Kategorie(Base):
    __tablename__ = "kategorie"

    kategorie_id = Column(Integer, primary_key=True, autoincrement=True)
    nazev = Column(String(64), nullable=False)
    rocnik_od = Column(YEAR, nullable=True)
    rocnik_do = Column(YEAR, nullable=True)

    # vazba: jedna kategorie → více závodníků
    zavodnici = relationship("Zavodnik", back_populates="kategorie")


class Trener(Base):
    __tablename__ = "treneri"

    trener_id = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String(128), nullable=False, default="Neuveden")

    # vazba: trenér → více závodníků
    zavodnici = relationship("Zavodnik", back_populates="trener")

class Znamky(Base):
    __tablename__ = "znamky"

    zavodnik_id = Column(Integer, ForeignKey("zavodnici.zavodnik_id"), primary_key=True)
    naradi_id = Column(Integer, ForeignKey("naradi.naradi_id"), primary_key=True)
    znamka_D = Column(Numeric(12, 4), nullable=False, default=0)
    pen = Column(Numeric(12, 4), nullable=False, default=0)
    srazky_E = Column(Numeric(12, 4), nullable=False, default=0)
    vysledna = Column(Numeric(12, 4), nullable=False)

    zavodnik = relationship("Zavodnik", back_populates="znamky")
    naradi = relationship("Naradi")

class Zavodnik(Base):
    __tablename__ = "zavodnici"

    zavodnik_id = Column(Integer, primary_key=True, autoincrement=True)
    kategorie_id = Column(Integer, ForeignKey("kategorie.kategorie_id"), nullable=False)
    rocnik = Column(YEAR, nullable=False)
    oddil_id = Column(Integer, ForeignKey("oddily.oddil_id"), nullable=False)
    trener_id = Column(Integer, ForeignKey("treneri.trener_id"), nullable=False)
    druzstvo = Column(SmallInteger, nullable=False)
    jmeno = Column(String(128), nullable=False)
    gis_id = Column(Integer, nullable=True)

    # vazby na rodiče
    kategorie = relationship("Kategorie", back_populates="zavodnici")
    trener = relationship("Trener", back_populates="zavodnici")
    oddil = relationship("Oddil", back_populates="zavodnici")
    znamky = relationship("Znamky", back_populates="zavodnik", cascade="all, delete-orphan")

class Naradi(Base):
    __tablename__ = "naradi"

    naradi_id = Column(Integer, primary_key=True, autoincrement=True)
    naradi = Column(String(64), nullable=False)
    obrazek = Column(LargeBinary, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    # vazba: naradi -> vice rozhodcich
    rozhodci = relationship("Rozhodci", back_populates="naradi")
    znamky = relationship("Znamky", back_populates="naradi", cascade="all, delete-orphan")

class Rozhodci(Base):
    __tablename__ = "rozhodci"

    rozhodci_id = Column(Integer, primary_key=True, autoincrement=True)
    jmeno = Column(String(128), nullable=False)
    naradi_id = Column(Integer, ForeignKey("naradi.naradi_id"), nullable=True)
    oddil = Column(String(128), nullable=True)
    poznamka = Column(String(128), nullable=True)
    rozhodci_typ = Column(CHAR(1), nullable=True)

    # vazba na rodiče
    naradi = relationship("Naradi", back_populates="rozhodci")

class Oddil(Base):
    __tablename__ = "oddily"

    oddil_id = Column(Integer, primary_key=True, autoincrement=True)
    nazev = Column(String(128), nullable=False)

    # vazba: trenér → více závodníků
    zavodnici = relationship("Zavodnik", back_populates="oddil")

#------- views ----------#

#class VVysledky(Base):
#    __tablename__ = "v_vysledky"
#    __table_args__ = {"autoload_with": engine}

#    zavodnik_id = Column(Integer, primary_key=True)
 #   naradi = Column(String, primary_key=True)