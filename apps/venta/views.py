from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import Venta
from datetime import date
from django.db.models import Q
from datetime import datetime


def generate_pdf(request, filtro=None):
    try:
        fecha_inicial = request.GET.get('fecha_inicial', None)
        fecha_final = request.GET.get('fecha_final', None)

        # Filtrar ventas según los parámetros proporcionados
        ventas = Venta.objects.all()

        # Verificar si se proporcionaron fechas y aplicar los filtros correspondientes
        if fecha_inicial:
            if fecha_final:
                ventas = ventas.filter(fecha_venta__range=(fecha_inicial, fecha_final))
            else:
                fecha_final= datetime.now()
                ventas = ventas.filter(fecha_venta__range=(fecha_inicial, fecha_final))


        # Verificar qué parámetros se han proporcionado y aplicar los filtros correspondientes
        if filtro:
            ventas = ventas.filter(Q(id_venta__icontains=filtro) | Q(no_documento_usuario_fk__nombre_usuario__icontains=filtro)| Q(no_documento_usuario_fk__apellido_usuario__icontains=filtro))    


        # Crear un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Definir el nombre del archivo PDF
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.pdf"'

        # Crear un objeto SimpleDocTemplate para generar el PDF
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Configurar los estilos
        styles = getSampleStyleSheet()
        style_heading = styles['Heading1']
        style_body = styles['BodyText']

        # Crear una lista de elementos Platypus para agregar al PDF
        elements = []

        # Agregar el texto "Logo empresarial" en la esquina superior izquierda
        elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#732F48'))))

        # Agregar la fecha en la esquina superior derecha
        elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=10, alignment=2)))

        # Agregar el título en el centro
        elements.append(Paragraph("<br/><br/><br/>Reporte de Ventas", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

        # Agregar el filtro utilizado
        filter_info = f"Filtro: filtro='{filtro},fecha inicial{fecha_inicial}, fecha final{fecha_final}"
        elements.append(Paragraph(filter_info, style_body))
        elements.append(Spacer(1, 12))  # Espacio entre el filtro y la tabla

        # Agregar espacio entre el título y la tabla
        elements.append(Spacer(1, 36))

        # Agregar los detalles de cada venta al documento
        data = [["N° Venta", "Fecha Venta", "Hora Venta", "Total Venta", "Documento Usuario", "Estado"]]
        for venta in ventas:
            data.append([
                venta.id_venta,
                venta.fecha_venta.strftime('%d/%m/%Y'),
                venta.hora_venta.strftime('%H:%M:%S'),
                venta.total_venta,
                f"{venta.no_documento_usuario_fk.nombre_usuario} {venta.no_documento_usuario_fk.apellido_usuario}" if venta.no_documento_usuario_fk else "",
                'Activo' if venta.estado else 'Inactivo'
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
    except Exception as e:
        # En caso de error, devolver una respuesta de error
        return HttpResponse(f"Ocurrió un error: {str(e)}", status=500)
