from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .models import DetalleVenta, Venta
from datetime import date 
from django.shortcuts import get_object_or_404

def generate_pdf(request, id_venta=None):
    try:
        # Obtener la información de la venta según el id_venta proporcionado
        venta = get_object_or_404(Venta, id_venta=id_venta)
        detalles_venta = DetalleVenta.objects.filter(id_venta_fk=venta)

        # Crear un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        # Define el nombre del archivo PDF
        response['Content-Disposition'] = f'attachment; filename="comprobante_pago_venta_{id_venta}.pdf"'

        # Crear un objeto SimpleDocTemplate para generar el PDF
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Crear una lista de elementos Platypus para agregar al PDF
        elements = []

        # Agregar el texto "Logo empresarial" en la esquina superior izquierda
        elements.append(Paragraph("Logo empresarial", ParagraphStyle(name='LogoStyle', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#732F48'))))

        # Agregar la fecha en la esquina superior derecha
        elements.append(Paragraph(f"{date.today().strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica-Bold', fontSize=10, alignment=2)))

        # Agregar el título en el centro con el id_venta
        elements.append(Paragraph(f"<br/><br/><br/>Comprobante de Pago - Factura: {id_venta}", ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=16, textColor=colors.HexColor('#8C274C'), alignment=1)))
        
        # Agregar espacio entre el título y la fecha de emisión del comprobante
        elements.append(Spacer(1, 12))

    
        # Agregar día de la venta
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Día de la venta: {venta.fecha_venta.strftime('%d/%m/%Y')}", ParagraphStyle(name='DateStyle', fontName='Helvetica', fontSize=12, textColor=colors.black)))

        # Agregar espacio entre la fecha de emisión del comprobante y la información del cliente
        elements.append(Spacer(1, 12))

        # Crear una tabla para la información del cliente
        table_data = [
            ["Informacion del Cliente"],
            ["ID Venta:", f"{id_venta}"],
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

        # Agregar espacio entre la información del cliente y los detalles de la venta
        elements.append(Spacer(1, 24))

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
    except Exception as e:
        # En caso de error, devolver una respuesta de error
        return HttpResponse(f"Ocurrió un error: {str(e)}", status=500)
