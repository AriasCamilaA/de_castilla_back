from django.db import models
from apps.insumo.models import Insumo
from apps.producto.models import Producto
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from datetime import date
from .models import Inventario
from reportlab.lib.units import inch
from django.db.models import Q

def generate_pdf(request, filtro=None):
    # Obtener todos los registros de inventario desde la base de datos
    inventario = Inventario.objects.all()

    if filtro:
        inventario = inventario.filter(
            Q(id_inventario__icontains=filtro) |
            Q(stock_inventario__icontains=filtro) |
            Q(tipo_inventario__icontains=filtro) |
            Q(id_insumo_fk__nombre_insumo__icontains=filtro) |
            Q(id_producto_fk__nombre_producto__icontains=filtro)
        )

    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Definir el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    # Crear un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Configurar los estilos de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#732F48')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F6E0E3')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8C274C'))
    ])

    # Crear una lista de elementos Platypus para agregar al PDF
    elements = []

    # Agregar el texto "Logo empresarial" en la esquina superior izquierda
    elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#732F48'))))

    # Agregar la fecha en la esquina superior derecha
    elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=8, alignment=2)))

    # Agregar el título en el centro
    elements.append(Paragraph("<br/><br/><br/>Reporte de Inventario", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#8C274C'), alignment=1)))

    # Agregar espacio entre el título y la tabla
    elements.append(Spacer(1, 12))

    # Crear una lista de datos para la tabla de contenido
    data = [["ID", "Stock", "Tipo", "Insumo/Producto"]]
    for i in inventario:
        # Obtener el nombre del insumo o producto
        nombre_insumo_producto = i.id_insumo_fk.nombre_insumo if i.id_insumo_fk else i.id_producto_fk.nombre_producto
        # Agregar los detalles del inventario al documento
        data.append([str(i.id_inventario), str(i.stock_inventario), i.tipo_inventario, nombre_insumo_producto])

    # Crear la tabla con los datos y aplicar los estilos
    table = Table(data)
    table.setStyle(style)
    table._argW[3] = 1.5 * inch  # Ajustar el ancho de la columna Insumo/Producto

    # Agregar la tabla al documento
    elements.append(table)

    # Construir el PDF
    doc.build(elements)

    # Devolver la respuesta con el PDF generado
    return response
