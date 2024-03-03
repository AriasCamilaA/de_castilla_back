from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from .models import DetalleOC
from datetime import date

def generate_pdf(request):
    # Obtener todos los detalles de órdenes de compra desde la base de datos
    detalles_oc = DetalleOC.objects.all()

    # Crea un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Define el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_detalles_oc.pdf"'

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
    elements.append(Paragraph("<br/><br/><br/>Detalle de Ordeden de Compra", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

    elements.append(Spacer(1, 36))  # Agrega espacio después del encabezado

    # Crea una tabla para mostrar los detalles de órdenes de compra
    data = [["N° Detalle OC", "N° Orden Compra", "N° Insumo","Cantidad Insumo", "Estado"]]
    for detalle_oc in detalles_oc:
        data.append([
            detalle_oc.id_detalle_oc,
            detalle_oc.id_oc_fk_id,
            detalle_oc.id_insumo_fk_id,
            detalle_oc.cantidad_insumo,
            'Activo' if detalle_oc.estado else 'Inactivo'
        ])

    # Crea la tabla y define su estilo
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#732F48')),  # Color del encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),  # Color del texto del encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación del texto
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F6E0E3')),  # Color de fondo de las filas
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8C274C'))  # Color de las líneas de la tabla
    ]))

    # Agrega la tabla al documento
    elements.append(table)

    # Genera el PDF
    doc.build(elements)

    # Devuelve la respuesta con el PDF generado
    return response
