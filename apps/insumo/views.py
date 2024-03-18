from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .models import Insumo
from django.utils.html import escape as html_escape 
from datetime import date 
from django.db.models import Q
import os 

def generate_pdf(request, filtro=None):
    try:
        # Obtener todos los insumos desde la base de datos
        insumos = Insumo.objects.all()

        # Filtrar insumos si se proporciona un filtro
        if filtro:
            insumos = insumos.filter(Q(nombre_insumo__icontains=filtro))
            filtro_texto = f"Filtro = {filtro}"
        else:
            filtro_texto = ""

        # Crear un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Define el nombre del archivo PDF
        response['Content-Disposition'] = 'attachment; filename="reporte_insumos.pdf"'

        # Crea un objeto SimpleDocTemplate para generar el PDF
        doc = SimpleDocTemplate(response, pagesize=letter)

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
            elements.append(Paragraph("<br/><br/><br/>Reporte de Insumo", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

            # Agregar el texto del filtro si se aplicó
            if filtro_texto:
                elements.append(Spacer(1, 10))
                elements.append(Paragraph(filtro_texto, ParagraphStyle(name='FilterStyle', fontName='Helvetica', fontSize=12)))

            # Agregar espacio entre el título/filtro y la tabla
            elements.append(Spacer(1, 36))
            # Crear una lista de datos para la tabla de contenido
            data = [
                ["N° Insumo", "Nombre", "Estado"]
            ]
            # Agregar los datos de cada insumo a la lista de datos
            for insumo in insumos:
                data.append([
                    str(insumo.id_insumo),
                    html_escape(insumo.nombre_insumo),  # Usamos html_escape en lugar de escape
                    'Activo' if insumo.estado else 'Inactivo',
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

            # Agregar la tabla a los elementos del PDF
            elements.append(table)

            # Generar el PDF
            doc.build(elements)

            # Devolver la respuesta con el PDF generado
            return response
        else:
            return HttpResponse("La imagen del logo no se pudo encontrar.", status=404)

    except Exception as e:
        # En caso de error, devolver una respuesta de error
        return HttpResponse(f"Ocurrió un error: {str(e)}", status=500)
