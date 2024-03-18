from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
from .models import Usuario
from datetime import date
import os

def generate_pdf(request):
    # Obtener todos los usuarios desde la base de datos
    usuarios = Usuario.objects.all()

    # Crea un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Define el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_usuarios.pdf"'

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

        # Crea una lista de elementos Platypus para agregar al PDF
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
        elements.append(Paragraph("<br/><br/><br/>Reporte de Usuarios", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

        # Agregar espacio entre el título y la tabla
        elements.append(Spacer(1, 36))

        # Agrega los detalles de cada usuario al documento
        data = [["N° Documento", "Nombre", "Apellido", "Correo Electrónico", "Rol", "Estado"]]
        for usuario in usuarios:
            data.append([
                usuario.no_documento_usuario,
                usuario.nombre_usuario,
                usuario.apellido_usuario,
                usuario.email,
                usuario.id_rol_fk.nombre_rol if usuario.id_rol_fk else "",
                'Activo' if usuario.estado else 'Inactivo'
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
    else:
            return HttpResponse("La imagen del logo no se pudo encontrar.", status=404)
 
    # Genera el PDF
    doc.build(elements)

    # Devuelve la respuesta con el PDF generado
    return response
