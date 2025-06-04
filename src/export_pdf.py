import os

from pathlib import Path
from fpdf import FPDF

pdf_base_path = os.getenv("PDF_EXPORT_BASE_PATH")

def export_pdf(query, results):
    pdf_path = Path(pdf_base_path + "export.pdf")
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Search results for '{query}'", ln=True, align="C")
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(10, 10, "No.", border=1)
        pdf.cell(80, 10, "Case Name", border=1)
        pdf.cell(30, 10, "Date Filed", border=1)
        pdf.ln()
    
        # Data rows
        pdf.set_font("Arial", size=11)
        for idx, item in enumerate(results, start=1):
            name = (item.get("caseName", "-"))[:40]
            date_filed = item.get("dateFiled", "-")
            pdf.cell(10, 10, str(idx), border=1)
            pdf.cell(80, 10, name, border=1)
            pdf.cell(30, 10, date_filed, border=1)
            pdf.ln()
    
        pdf.output(str(pdf_path))
    except Exception as e:
        raise e