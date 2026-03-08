from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm


class VysledkyService:

    @staticmethod
    def generate_pdf(*, year: str,competition: str, path: str, data: dict):


        naradi = sorted(data["naradi"], key=lambda x: x[0])  # řazení dle id
        kategorie_dict = data["kategorie"]

        pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", "DejaVuSans-Bold.ttf"))

        normal_style = ParagraphStyle(
            name="Normal",
            fontName="DejaVu",
            fontSize=6,
            leading=9
        )

        bold_style = ParagraphStyle(
            name="Bold",
            fontName="DejaVu-Bold",
            fontSize=6,
            leading=9
        )

        doc = SimpleDocTemplate(
            path,
            pagesize=landscape(A4),
            rightMargin=10,
            leftMargin=10,
            topMargin=15,
            bottomMargin=15
        )

        elements = []

        for kategorie, zavodnici in kategorie_dict.items():

            elements.append(Paragraph(f"{competition} {year}", bold_style))
            elements.append(Paragraph(f"Kategorie: {kategorie}", bold_style))
            elements.append(Spacer(1, 5))

            table_data = []

            # ===============================
            # 1️⃣ HLAVIČKA – název nářadí
            # ===============================
            header_1 = ["Um.", "Jméno", "Ročník", "Oddíl", "Trenér"]

            for _, nazev in naradi:
                header_1.extend([nazev, "", "", ""])

            header_1.append("Celkem")

            # ===============================
            # 2️⃣ HLAVIČKA – D E Pen Vysl
            # ===============================
            header_2 = ["", "", "", "", ""]

            for _ in naradi:
                header_2.extend(["D", "E", "Pen", "Vysl"])

            header_2.append("")

            table_data.append(header_1)
            table_data.append(header_2)

            # ===============================
            # DATA
            # ===============================
            for poradi, z in enumerate(zavodnici, start=1):

                row = [
                    poradi,
                    Paragraph(z["jmeno"], normal_style),
                    z["rocnik"],
                    Paragraph(z["oddil"], normal_style),
                    Paragraph(z["trener"], normal_style)
                ]

                def fmt(val):
                    if val in (None, ""):
                        return ""
                    return f"{val:.2f}"

                for nar_id, _ in naradi:
                    nar = z["naradi"].get(nar_id, {})
                    row.extend([
                        fmt(nar.get("D")),
                        fmt(nar.get("E")),
                        fmt(nar.get("Pen")),
                        fmt(nar.get("Vysl"))
                    ])

                row.append(Paragraph(fmt(z["celkem"]), bold_style))


                table_data.append(row)

            # ===============================
            # ŠÍŘKY SLOUPCŮ (musí se vejít!)
            # ===============================

            # dostupná šířka stránky
            page_width, _ = landscape(A4)
            usable_width = page_width - doc.leftMargin - doc.rightMargin

            # pevné sloupce
            fixed_cols = [12 * mm, 32 * mm, 15 * mm, 32 * mm, 28 * mm]  # můžeš jemně doladit
            fixed_total = sum(fixed_cols)

            celkem_width = 18 * mm

            # kolik zbývá na nářadí
            remaining_width = usable_width - fixed_total - celkem_width

            # šířka jednoho nářadí (4 sloupce D,E,Pen,Vysl)
            naradi_block_width = remaining_width / len(naradi)

            # rozdělíme rovnoměrně mezi D,E,Pen,Vysl
            single_col = naradi_block_width / 4

            col_widths = fixed_cols.copy()

            for _ in naradi:
                col_widths.extend([single_col] * 4)

            col_widths.append(celkem_width)

            table = Table(
                table_data,
                colWidths=col_widths,
                repeatRows=2
            )

            # ===============================
            # STYL
            # ===============================

            style = [
                ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BACKGROUND", (0, 0), (-1, 1), colors.lightgrey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),
                ("FONTSIZE", (0, 0), (-1, -1), 6),
            ]

            # SPAN prvních 5 sloupců přes 2 řádky
            for col in range(5):
                style.append(("SPAN", (col, 0), (col, 1)))

            # SPAN nářadí v prvním řádku
            start = 5
            for _ in naradi:
                style.append(("SPAN", (start, 0), (start+3, 0)))
                start += 4

            # SPAN Celkem
            style.append(("SPAN", (start, 0), (start, 1)))

            # zvýraznění Celkem
            style.append(("BACKGROUND", (start, 2), (start, -1), colors.whitesmoke))

            table.setStyle(TableStyle(style))

            elements.append(table)
            elements.append(PageBreak())

        doc.build(elements)

