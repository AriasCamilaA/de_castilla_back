from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .models import DetalleVenta, Venta
from datetime import date 
from django.shortcuts import get_object_or_404
import os

def generate_pdf(request, id_venta=None):
    try:
        # Obtener la venta correspondiente al ID proporcionado o devolver 404 si no se encuentra
        venta = get_object_or_404(Venta, id_venta=id_venta)

        # Obtener los detalles de la venta filtrando por la venta específica
        detalles_venta = DetalleVenta.objects.filter(id_venta_fk=venta)

        # Crear un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Define el nombre del archivo PDF con el ID de la venta
        response['Content-Disposition'] = f'attachment; filename="comprobante_pago_venta_{venta.id_venta}.pdf"'

        # Crear un objeto SimpleDocTemplate para generar el PDF
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
            elements.append(Paragraph("<br/><br/><br/>Comprobante De Pago", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))
            elements.append(Spacer(1, 36))

            # Agregar día de la venta
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(f"Día de la venta: {venta.fecha_venta.strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=12, textColor=colors.black)))
           
            # Agregar espacio entre el título/filtro y la tabla
            elements.append(Spacer(1, 36))
           
            # Crear una tabla para la información del cliente
            table_data = [
                ["Informacion del Cliente"],
                ["N° Venta:", f"{venta.id_venta}"],
                ["Nombre:", f"{venta.no_documento_usuario_fk.nombre_usuario} {venta.no_documento_usuario_fk.apellido_usuario}"],
                ["Celular:", f"{venta.no_documento_usuario_fk.celular_usuario}"]
            ]
            
            table = Table(table_data, colWidths=[100, '*'])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8C274C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
            ]))
            elements.append(table)

            # Crear una tabla para los detalles de la venta
            detalles_data = [
                ["Detalles de la Venta"],
                ["Producto", "Cantidad", "Valor Unitario", "Subtotal"]
            ]
            total_venta = 0
            for detalle_venta in detalles_venta:
                subtotal = detalle_venta.subtotal_detalle_venta
                total_venta += subtotal
                detalles_data.append([
                    detalle_venta.id_producto_fk.nombre_producto,
                    detalle_venta.cantidad_producto,
                    detalle_venta.id_producto_fk.precio_producto,
                    subtotal
                ])
            detalles_data.append(["", "", "Total Venta:", total_venta])  # Agregar fila para el total de la venta
            detalles_table = Table(detalles_data, colWidths=[200, 100, 100, 100])
            detalles_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8C274C')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(detalles_table)

            # Generar el PDF
            doc.build(elements)

            # Devolver la respuesta con el PDF generado
            return response
        else:
            return HttpResponse("La imagen del logo no se pudo encontrar.", status=404)

    except Exception as e:
        # En caso de error, devolver una respuesta de error
        return HttpResponse(f"Ocurrió un error: {str(e)}", status=500)
