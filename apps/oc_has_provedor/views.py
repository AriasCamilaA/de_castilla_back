from django.shortcuts import render

# Create your views here.
from django.db import models
from apps.orden_compra.models import OrdenCompra
from apps.proveedor.models import Proveedor
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from django.http import HttpResponse
from datetime import date
from .models import OCHasProveedor
from reportlab.lib.units import inch

def generate_pdf(request):
    # Obtener todos los registros de la relación OC - Proveedor desde la base de datos
    oc_proveedor = OCHasProveedor.objects.all()

    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Definir el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_oc_proveedor.pdf"'

    # Crear un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Configurar los estilos de la tabla
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#732F48')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F6E0E3')),
                        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8C274C'))])

    # Crear una lista de elementos Platypus para agregar al PDF
    elements = []

    # Agregar el texto "Logo empresarial" en la esquina superior izquierda
    elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#732F48'))))

    # Agregar la fecha en la esquina superior derecha
    elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=8, alignment=2)))

    # Agregar el título en el centro
    elements.append(Paragraph("<br/><br/><br/>Reporte de Órdenes de Compra por Proveedor", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#8C274C'), alignment=1)))

    # Agregar espacio entre el título y la tabla
    elements.append(Spacer(1, 18))

    # Agregar los registros al PDF
    data = [["N° OC", "Proveedor"]]
    for oc_prov in oc_proveedor:
        # Obtener el nombre del proveedor
        nombre_proveedor = oc_prov.id_proveedor_fk.nombre_proveedor if oc_prov.id_proveedor_fk else ""
        # Agregar los detalles de la relación OC - Proveedor al documento
        data.append([str(oc_prov.id_oc_fk.id_oc), nombre_proveedor])

    # Crear la tabla con los datos y aplicar los estilos
    table = Table(data)
    table.setStyle(style)

    # Agregar la tabla al documento
    elements.append(table)

    # Construir el PDF
    doc.build(elements)

    # Devolver la respuesta con el PDF generado
    return response
