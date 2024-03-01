from django.shortcuts import render

# Create your views here.
from django.db import models
from apps.insumo.models import Insumo
from apps.producto.models import Producto
from apps.tipo_movimiento.models import TipoMovimiento
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from datetime import date
from .models import Historico
from reportlab.lib.units import inch

def generate_pdf(request):
    # Obtener todos los registros del historial desde la base de datos
    historial = Historico.objects.all()

    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Definir el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_historico.pdf"'

    # Crear un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Configurar los estilos de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#732F48')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Reducir el espaciado inferior de las celdas
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F6E0E3')),
                        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8C274C'))])

    # Crear una lista de elementos Platypus para agregar al PDF
    elements = []

    # Agregar el texto "Logo empresarial" en la esquina superior izquierda
    elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#732F48'))))  # Reducir el tamaño de la fuente

    # Agregar la fecha en la esquina superior derecha
    elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=8, alignment=2)))  # Reducir el tamaño de la fuente

    # Agregar el título en el centro
    elements.append(Paragraph("<br/><br/><br/>Reporte de Ventas", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#8C274C'), alignment=1)))  # Reducir el tamaño de la fuente

    # Agregar espacio entre el título y la tabla
    elements.append(Spacer(1, 18))  # Reducir el espacio entre el título y la tabla

    # Agregar los registros al PDF
    data = [["N°", "Cantidad", "Fecha de Caducidad", "Fecha de Movimiento", "Tipo", "Insumo/Producto"]]
    for h in historial:
        # Obtener el nombre del insumo o producto
        nombre_insumo_producto = h.id_insumo_fk.nombre_insumo if h.id_insumo_fk else h.id_producto_fk.nombre_producto
        # Agregar los detalles del historial al documento
        data.append([str(h.id_historico), str(h.cantidad_historico), str(h.fecha_caducidad), str(h.fecha_movimiento), h.tipo_historico, nombre_insumo_producto])

    # Crear la tabla con los datos y aplicar los estilos
    table = Table(data)
    table.setStyle(style)
    table._argW[4] = 1 * inch  # Ajustar el ancho de la columna Insumo/Producto

    # Agregar la tabla al documento
    elements.append(table)

    # Construir el PDF
    doc.build(elements)

    # Devolver la respuesta con el PDF generado
    return response
