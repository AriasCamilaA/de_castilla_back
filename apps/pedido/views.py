from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import Pedido
from datetime import date
from django.db.models import Q
from datetime import datetime
import os

def generate_pdf(request, filtro=None):

    try:
        fecha_inicial = request.GET.get('fecha_inicial', None)
        fecha_final = request.GET.get('fecha_final', None)

        # Obtener todos los objetos de Pedido desde la base de datos
        pedidos = Pedido.objects.all()

        if fecha_inicial:
            if not fecha_final:
                fecha_final = datetime.now().date()
            pedidos = pedidos.filter(fecha_pedido__range=(fecha_inicial, fecha_final))

        if filtro:
            pedidos = pedidos.filter(Q( id_pedido__icontains=filtro) | Q(no_Documento_Usuario_fk__nombre_usuario__icontains=filtro) | Q(no_Documento_Usuario_fk__no_documento_usuario__icontains=filtro))
            filtro_texto = f"Filtro = {filtro}"
        else:
            filtro_texto = ""


        # Crea un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Define el nombre del archivo PDF
        response['Content-Disposition'] = 'attachment; filename="reporte_pedidos.pdf"'

        # Crea un objeto SimpleDocTemplate para generar el PDF
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Configurar los estilos
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
            elements.append(Paragraph("<br/><br/><br/>Reporte de Pedidos", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

            # Agregar el texto del filtro si se aplicó
            if filtro_texto:
                elements.append(Spacer(1, 10))
                elements.append(Paragraph(filtro_texto, ParagraphStyle(name='FilterStyle', fontName='Helvetica', fontSize=12)))

            # Agregar espacio entre el título/filtro y la tabla
            elements.append(Spacer(1, 36))
       
            # Crear una lista de datos para el contenido principal
            data = [
                ["N° Pedido", "Descripción", "Fecha", "Estado", "Documento", "Cliente"]
            ]
            # Agregar los datos de cada pedido a la lista de datos
            for pedido in pedidos:
                data.append([
                    str(pedido.id_pedido),
                    pedido.descripcion_pedido,
                    str(pedido.fecha_pedido),
                    pedido.id_estado_pedido_fk.nombre_estado if pedido.id_estado_pedido_fk else "N/A",  
                    pedido.no_Documento_Usuario_fk.no_documento_usuario if pedido.no_Documento_Usuario_fk else "N/A", 
                    f"{pedido.no_Documento_Usuario_fk.nombre_usuario} {pedido.no_Documento_Usuario_fk.apellido_usuario}" if pedido.no_Documento_Usuario_fk else "",
                ])

            # Crear una tabla y definir su estilo
            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#732F48')),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#ffffff')),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F6E0E3')),
                                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#8C274C'))])

            # Aplicar el estilo a la tabla
            table.setStyle(style)

            # Agregar la tabla al contenido
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
