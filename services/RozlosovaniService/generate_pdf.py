from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class RozlosovaniService:

    @staticmethod
    def generate_pdf(*, path: str, data: list[dict]):

        # -------------------------------------------------
        # FONT – diakritika
        # -------------------------------------------------
        pdfmetrics.registerFont(
            TTFont(
                "DejaVu",
                "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
            )
        )

        # -------------------------------------------------
        # DOKUMENT
        # -------------------------------------------------
        doc = SimpleDocTemplate(
            path,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
        )

        # -------------------------------------------------
        # STYLY
        # -------------------------------------------------
        header_style = ParagraphStyle(
            name="Header",
            fontName="DejaVu",
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12,
        )

        cell_style = ParagraphStyle(
            name="Cell",
            fontName="DejaVu",
            fontSize=10,
        )

        story = []

        # -------------------------------------------------
        # OBSAH
        # -------------------------------------------------
        for team in data:
            block = []

            # Nadpis družstva
            block.append(
                Paragraph(team["druzstvo"], header_style)
            )

            # Tabulka
            table_data = [
                ["Jméno", "Ročník", "Oddíl"]
            ]

            for z in team["zavodnici"]:
                table_data.append([
                    Paragraph(z["jmeno"], cell_style),
                    Paragraph(str(z["rocnik"]), cell_style),
                    Paragraph(z["oddil"], cell_style),
                ])

            table = Table(
                table_data,
                colWidths=[70 * mm, 25 * mm, 70 * mm],
                repeatRows=1,
            )

            table.setStyle(TableStyle([
                ("FONT", (0, 0), (-1, -1), "DejaVu"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
            ]))

            block.append(table)
            block.append(Spacer(1, 12))

            # ZÁSADNÍ – nerozdělí družstvo
            story.append(KeepTogether(block))

        # -------------------------------------------------
        # BUILD
        # -------------------------------------------------
        doc.build(story)

