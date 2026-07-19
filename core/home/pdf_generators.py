import os
import tempfile
from django.template.loader import render_to_string
from pyhtml2pdf import converter
import uuid

def generate_pdf_with_pyhtml2pdf(data, output_path="report.pdf", title="Data Report"):
    """
    Renders a Django HTML template and converts it to a PDF using pyhtml2pdf.
    """
    if not data:
        raise ValueError("The data list cannot be empty.")

    headers = list(data[0].keys())
    context = {
        'title': title,
        'headers': headers,
        'data': data
    }
    html_string = render_to_string('pdf_template.html', context)
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as temp_html:
        temp_html.write(html_string)
        temp_html_path = temp_html.name

    try:
        file_url = f"file:///{os.path.abspath(temp_html_path)}"
        converter.convert(file_url, f"reports/{uuid.uuid4()}.pdf")
        
    finally:
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
            
    return output_path