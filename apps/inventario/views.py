from django.db import models
from apps.insumo.models import Insumo
from apps.producto.models import Producto
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from datetime import date
from .models import Inventario
from django.db.models import Q
import os

def generate_pdf(request, filtro=None):
    # Obtener todos los registros de inventario desde la base de datos
    inventario = Inventario.objects.all()

    if filtro:
        inventario = inventario.filter(Q(id_inventario__icontains=filtro) | Q(stock_inventario__icontains=filtro) | Q(tipo_inventario__icontains=filtro) | Q(id_insumo_fk__nombre_insumo__icontains=filtro) | Q(id_producto_fk__nombre_producto__icontains=filtro))
        filtro_texto = f"Filtro = {filtro}"
    else:
        filtro_texto = ""

    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Definir el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    # Crear un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Configurar los estilos
    styles = getSampleStyleSheet()
    style_heading = styles['Heading1']
    style_body = styles['BodyText']

    # Ruta completa de la imagen
    image_path = os.path.join(os.path.dirname(__file__), '../../media/logo/logo_letra_oscura.png')

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

    try:
        # Verificar si la imagen existe en la ruta especificada
        if os.path.exists(image_path):
            # Crear una lista de elementos Platypus para agregar al PDF
            elements = []

            # Crear una tabla con dos columnas para la imagen y la fecha
            table_data = [
                [Image(image_path, width=70, height=50), Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=10, alignment=2))]
            ]
            table = Table(table_data, colWidths=[100, 400])  # Ancho de las columnas
            elements.append(table)

            # Agregar espacio entre la imagen/fecha y el título de la tabla
            elements.append(Spacer(1, 10))

            # Agregar el título en el centro
            elements.append(Paragraph("<br/><br/><br/>Reporte de Inventario", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

            # Agregar el texto del filtro si se aplicó
            if filtro_texto:
                elements.append(Spacer(1, 10))
                elements.append(Paragraph(filtro_texto, ParagraphStyle(name='FilterStyle', fontName='Helvetica', fontSize=12)))

            # Agregar espacio entre el título/filtro y la tabla
            elements.append(Spacer(1, 36))

            # Crear una lista de datos para la tabla de contenido
            data = [["ID", "Stock", "Tipo", "Insumo/Producto"]]
            for i in inventario:
                # Obtener el nombre del insumo o producto
                nombre_insumo_producto = i.id_insumo_fk.nombre_insumo if i.id_insumo_fk else i.id_producto_fk.nombre_producto
                # Agregar los detalles del inventario al documento
                data.append([str(i.id_inventario), str(i.stock_inventario), i.tipo_inventario, nombre_insumo_producto])

            # Crear la tabla con los datos y aplicar los estilos, tambien se agrega el ancho de una columna
            table = Table(data)
            table.setStyle(style)
            table._argW[3] = 3 * 72  
            elements.append(table)

            # Construir el PDF
            doc.build(elements)

            # Devolver la respuesta con el PDF generado
            return response
        else:
            return HttpResponse("La imagen del logo no se pudo encontrar.", status=404)

    except Exception as e:
        # En caso de error, devolver una respuesta de error
        return HttpResponse(f"Ocurrió un error: {str(e)}", status=500)
