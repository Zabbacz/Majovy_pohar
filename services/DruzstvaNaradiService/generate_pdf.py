from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    KeepTogether,
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm


class DruzstvaNaradiService:

    @staticmethod
    def generate_pdf(path: str, data):

        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", "DejaVuSans-Bold.ttf"))

        normal = ParagraphStyle(
            name="Normal",
            fontName="DejaVu",
            fontSize=7,
            leading=9
        )

        bold = ParagraphStyle(
            name="Bold",
            fontName="DejaVu-Bold",
            fontSize=7,
            leading=9
        )

        def P(text, style):
            return Paragraph(str(text), style)

        doc = SimpleDocTemplate(
            path,
            pagesize=landscape(A4),
            leftMargin=10,
            rightMargin=10,
            topMargin=15,
            bottomMargin=15
        )

        elements = []

        col_widths = [
            70*mm,
            30*mm,
            25*mm,
            25*mm,
            25*mm,
            25*mm,
            25*mm,
            35*mm
        ]
        print(data)
        story = []

        for naradi in data:

            naradi_name = naradi["naradi"]

            for d in naradi["druzstva"]:
                block = []

                #kategorie = d("kategorie_id", "")
                druzstvo = d["druzstvo"]
                zavodnici = d["zavodnici"]
                kategorie = d["kategorie"]

                header = [
                    P(f"{naradi_name}<br/>Družstvo {druzstvo} - {kategorie}", bold),
                    P("Znamka D", bold),
                    P("Pen", bold),
                    P("Srážky E1", bold),
                    P("Srážky E2", bold),
                    P("Srážky E3", bold),
                    P("Průměr E", bold),
                    P("Výsledná", bold),
                ]
                table_data = [header]

                for jmeno in zavodnici:
                    table_data.append(
                        [P(jmeno, normal)] + [""] * 7
                    )

                table_data.append([
                    P("Podpis E1", bold),
                    "",
                    P("Podpis E2", bold),
                    "",
                    P("Podpis E3", bold),
                    "",
                    P("Podpis D", bold),
                    ""
                ])

                row_heights = (
                    [15*mm] +
                    [10*mm] * len(zavodnici) +
                    [18*mm]
                )

                table = Table(
                    table_data,
                    colWidths=col_widths,
                    rowHeights=row_heights
                )

                table.setStyle(TableStyle([
                    ("GRID", (0,0), (-1,-1), 1, colors.black),
                    ("ALIGN", (1,0), (-1,0), "CENTER"),
                    ("VALIGN", (0,0), (-1,0), "MIDDLE"),
                    ("ALIGN", (0,1), (0,-2), "LEFT"),
                    ("VALIGN", (0,1), (-1,-2), "MIDDLE"),
                    ("ALIGN", (0,-1), (-1,-1), "CENTER"),
                    ("VALIGN", (0,-1), (-1,-1), "MIDDLE"),
                ]))

                block.append(table)
                block.append(Spacer(1, 15))

                story.append(KeepTogether(block))

        doc.build(story)
