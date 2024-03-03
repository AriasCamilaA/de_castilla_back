from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from .models import EstadoPedido
from datetime import date

def generate_pdf(request):
    # Obtener todos los estados de pedido desde la base de datos
    estados_pedido = EstadoPedido.objects.all()

    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Define el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_estados_pedido.pdf"'

    # Crear un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Crear una lista de elementos Platypus para agregar al PDF
    elements = []

    # Agregar el texto "Logo empresarial" en la esquina superior izquierda
    elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#732F48'))))

    # Agregar la fecha en la esquina superior derecha
    elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=10, alignment=2)))

    # Agregar el título en el centro
    elements.append(Paragraph("<br/><br/><br/>Reporte de Estados de Pedido", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

    # Agregar espacio entre el título y la tabla
    elements.append(Spacer(1, 36))

    # Agregar los detalles de cada estado de pedido al documento
    data = [["N° Estado Pedido", "Estado Pedido", "Estado"]]
    for estado in estados_pedido:
        data.append([
            estado.id_estado_pedido,
            estado.nombre_estado,
            'Activo' if estado.estado else 'Inactivo'
        ])

    # Crear una tabla y definir su estilo
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#732F48')),  # Color del encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),  # Color del texto del encabezado
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación del texto
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente del encabezado
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado inferior del encabezado
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F6E0E3')),  # Color de fondo de las filas
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8C274C'))  # Color de las líneas de la tabla
    ]
    table = Table(data)
    table.setStyle(TableStyle(table_style))
    elements.append(table)

    # Generar el PDF
    doc.build(elements)

    # Devolver la respuesta con el PDF generado
    return response
