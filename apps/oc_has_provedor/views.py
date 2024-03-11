from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .models import OCHasProveedor
from datetime import date
from django.db.models import Q

def generate_pdf(request):
    try:
        nombre_proveedor = request.GET.get('nombre_proveedor', None)
        id_proveedor = request.GET.get('id_proveedor', None)

        # Filtrar registros de la relación OC - Proveedor según el nombre del proveedor proporcionado
        oc_proveedor = OCHasProveedor.objects.all()

        if nombre_proveedor:
            oc_proveedor = oc_proveedor.filter(id_proveedor_fk__nombre_proveedor__icontains=nombre_proveedor.strip())

        if id_proveedor:
            oc_proveedor = oc_proveedor.filter(id_proveedor_fk=id_proveedor.strip())


        # Crear un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Definir el nombre del archivo PDF
        response['Content-Disposition'] = 'attachment; filename="reporte_oc_proveedor.pdf"'

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
        elements.append(Paragraph("<br/><br/><br/>Reporte de Órdenes de Compra por Proveedor", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

        # Agregar el filtro utilizado
        filter_info = f"Filtro: nombre_proveedor='{nombre_proveedor}'"
        elements.append(Paragraph(filter_info, style_body))
        elements.append(Spacer(1, 12))  # Espacio entre el filtro y la tabla

        # Agregar espacio entre el título y la tabla
        elements.append(Spacer(1, 36))

        # Crear una lista de datos para el contenido principal
        data = [["N° OC", "Proveedor"]]
        for oc_prov in oc_proveedor:
            # Agregar los detalles de la relación OC - Proveedor al documento
            data.append([str(oc_prov.id_oc_fk.id_oc), oc_prov.id_proveedor_fk.nombre_proveedor if oc_prov.id_proveedor_fk else ""])

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
