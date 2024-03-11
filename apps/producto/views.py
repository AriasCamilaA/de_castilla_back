from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .models import Producto
from django.utils.html import escape as html_escape 
from datetime import date 
from django.db.models import Q

def generate_pdf(request, filtro=None):
    # Obtener todos los productos desde la base de datos
    productos = Producto.objects.all()

    if filtro:
        # Aplicar el filtro al nombre del producto o al ID de la categoría
        productos = productos.filter(Q(nombre_producto__icontains=filtro) | Q(id_categoria_fk__nombre_categoria__icontains=filtro)) 

    # Crear un objeto HttpResponse con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    # Define el nombre del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

    # Crea un objeto SimpleDocTemplate para generar el PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Crear una lista de elementos Platypus para agregar al PDF
    elements = []

    # Agregar el texto "Logo empresarial" en la esquina superior izquierda
    elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#732F48'))))

    # Agregar la fecha en la esquina superior derecha
    elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=10, alignment=2)))

    # Agregar el título en el centro
    elements.append(Paragraph("<br/><br/><br/>Reporte de Productos", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))

    filter_info = f"Filtro: filtro='{filtro}'"
    elements.append(Spacer(1, 12))

    # Agregar espacio entre el título y la tabla
    elements.append(Spacer(1, 36))

    # Crear una lista de datos para la tabla de contenido
    data = [
        ["N°", "Nombre", "Imagen", "Precio", "Categoría", "Estado"]
    ]
    # Agregar los datos de cada producto a la lista de datos
    for producto in productos:
        categoria_nombre = producto.id_categoria_fk.nombre_categoria if producto.id_categoria_fk else ""
        data.append([
            str(producto.id_producto),
            html_escape(producto.nombre_producto),
            producto.imagen_producto.url if producto.imagen_producto else "",
            str(producto.precio_producto),
            categoria_nombre,
            'Activo' if producto.estado else 'Inactivo',
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
