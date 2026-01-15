import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from app.models.schemas import FATProcedure

# Configure Jinja2 to look for templates in the templates directory
template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
env = Environment(loader=FileSystemLoader(template_dir))

def render_fat_pdf(procedure_data: FATProcedure) -> bytes:
    """
    Takes a validated FATProcedure object, renders it into the HTML template,
    and converts that HTML into a PDF byte stream.
    """
    
    # Load the template
    template = env.get_template("fat_template.html")
    
    # Render HTML with dynamic data
    html_content = template.render(
        data=procedure_data,
        date_generated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    # Generate PDF using WeasyPrint
    # We write to RAM (bytes) instead of disk to keep the container stateless
    pdf_bytes = HTML(string=html_content).write_pdf()
    
    return pdf_bytes