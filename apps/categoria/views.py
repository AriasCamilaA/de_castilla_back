# Create your views here.
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from .models import Categoria
from datetime import date

def generate_pdf(request):
    # Obtener todas las categorías desde la base de datos
    categorias = Categoria.objects.all()

    # Crea un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Define el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_categorias.pdf"'

    # Crea un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Define el estilo para el texto
    style = ParagraphStyle(name='Normal', fontSize=12, leading=14, textColor=colors.black)  # Estilo para el texto normal

    # Crea una lista de elementos Platypus para agregar al PDF
    elements = []

    # Agregar el texto "Logo empresarial" en la esquina superior izquierda
    elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#732F48'))))

    # Agregar la fecha en la esquina superior derecha
    elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=10, alignment=2)))

    # Agregar el título en el centro
    elements.append(Paragraph("<br/><br/><br/>Reporte de Categoria", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))


    # Iterar sobre las categorías y agregarlas al documento
    for categoria in categorias:
        # Define el texto con los datos de la categoría
        text = f"<br/><b>N° De producto:</b> {categoria.id_categoria}<br/><b>Nombre:</b> {categoria.nombre_categoria}<br/>Descripción: {categoria.descripcion_categoria}<br/>"

        # Agrega el texto al documento
        elements.append(Spacer(1, 12))  # Agrega un espacio entre cada categoría
        elements.append(Paragraph(text, style))

    # Genera el PDF
    doc.build(elements)

    # Devuelve la respuesta con el PDF generado
    return response
