from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image 
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from .models import Proveedor
from datetime import date
from django.db.models import Q
import os


def generate_pdf(request, filtro=None):
    try:
        # Obtener todos los proveedores desde la base de datos
        proveedores = Proveedor.objects.all()

        # Filtrar los proveedores si se proporciona un filtro
        if filtro:
            proveedores = proveedores.filter(Q(id_proveedor__icontains=filtro) | Q(empresa_proveedor__icontains=filtro) | Q(nombre_proveedor__icontains=filtro))

        # Crea un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Define el nombre del archivo PDF
        response['Content-Disposition'] = 'attachment; filename="reporte_de_proveedores.pdf"'

        # Crea un objeto SimpleDocTemplate para generar el PDF
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Configura los estilos
        styles = getSampleStyleSheet()
        style_heading = styles['Heading1']
        style_body = styles['BodyText']

        # Ruta completa de la imagen
        image_path = os.path.join(os.path.dirname(__file__), '../../media/logo/logo_letra_oscura.png')

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
            elements.append(Paragraph("<br/><br/><br/>Reporte de Ventas", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

            # Agregar espacio entre el título y la tabla
            elements.append(Spacer(1, 36))

            # Agregar el filtro utilizado
            if filtro:
                filter_info = f"Filtro: {filtro}"
                elements.append(Paragraph(filter_info, style_body))
                elements.append(Spacer(1, 12))  # Espacio entre el filtro y la tabla

            # Agregar espacio entre el título y la tabla
            elements.append(Spacer(1, 36))

            # Agrega los detalles de cada proveedor al documento
            data = [["Nombre", "Empresa", "Celular", "Correo Electrónico", "NIT", "Estado"]]
            for proveedor in proveedores:
                data.append([
                    proveedor.nombre_proveedor,
                    proveedor.empresa_proveedor,
                    proveedor.celular_proveedor,
                    proveedor.correo_proveedor,
                    proveedor.nit_proveedor,
                    'Activo' if proveedor.estado_proveedor else 'Inactivo'
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

            # Genera el PDF
            doc.build(elements)

            # Devuelve la respuesta con el PDF generado
            return response
        else:
            return HttpResponse("La imagen del logo no se pudo encontrar.", status=404)
    
    except Exception as e:
        # Manejar cualquier excepción que pueda ocurrir
        print(f"Error: {e}")
        # Devolver una respuesta de error
        return HttpResponse("Error al generar el PDF.")
