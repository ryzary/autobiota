from docx import Document
from docx.shared import Inches
import os

def generate_report(report_text: str, plot_paths: list = None, output_path="reports/report.docx") -> str:
    plot_paths = plot_paths or []

    doc = Document()
    doc.add_heading("Gut Microbiome Analysis Report", level=1)

    doc.add_paragraph(report_text)

    for path in plot_paths:
        if os.path.exists(path):
            doc.add_page_break()
            doc.add_picture(path, width=Inches(6.0))

    doc.save(output_path)
    return f"Report saved to {output_path}"

