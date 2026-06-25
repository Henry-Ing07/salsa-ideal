import io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from models.factura import Factura
from models.venta import Venta
from config import Config

ROJO_IDEAL = colors.HexColor("#E2342B")
VERDE_IDEAL = colors.HexColor("#1A7A4C")


class FacturasController:

    @staticmethod
    def listar():
        return Factura.listar()

    @staticmethod
    def obtener(factura_id):
        return Factura.obtener_por_id(factura_id)

    @staticmethod
    def generar_pdf(factura_id):
        factura = Factura.obtener_por_id(factura_id)
        if not factura:
            return None
        items = Venta.detalle_de_venta(factura["venta_id"])

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=letter,
            topMargin=2 * cm, bottomMargin=2 * cm,
            leftMargin=2 * cm, rightMargin=2 * cm,
        )
        styles = getSampleStyleSheet()
        titulo_style = ParagraphStyle(
            "Titulo", parent=styles["Title"], textColor=ROJO_IDEAL, fontSize=20
        )
        normal = styles["Normal"]

        elementos = []
        elementos.append(Paragraph(Config.EMPRESA_NOMBRE, titulo_style))
        elementos.append(Paragraph(f"NIT: {Config.EMPRESA_NIT}", normal))
        elementos.append(Paragraph(Config.EMPRESA_DIRECCION, normal))
        elementos.append(Spacer(1, 0.5 * cm))
        elementos.append(
            Paragraph(f"<b>Factura No.:</b> {factura['numero_factura']}", normal)
        )
        elementos.append(
            Paragraph(f"<b>Fecha:</b> {factura['fecha'].strftime('%Y-%m-%d %H:%M')}", normal)
        )
        elementos.append(Paragraph(f"<b>Cliente:</b> {factura['cliente']}", normal))
        vendedor = factura.get('vendedor_nombre') or 'N/A'
        rol = factura.get('vendedor_rol') or ''
        elementos.append(Paragraph(f"<b>Atendido por:</b> {vendedor} ({rol})", normal))
        elementos.append(Spacer(1, 0.5 * cm))

        def fmt(v):
            entero, _ = f"{float(v):,.2f}".split(".")
            return f"${entero.replace(',', '.')}"

        data = [["Producto", "Cantidad", "Precio Unit.", "Subtotal"]]
        for it in items:
            data.append([
                it["producto_nombre"],
                str(it["cantidad"]),
                fmt(it['precio']),
                fmt(it['cantidad'] * it['precio']),
            ])

        tabla = Table(data, colWidths=[7 * cm, 3 * cm, 3.5 * cm, 3.5 * cm])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), VERDE_IDEAL),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
        ]))
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.5 * cm))

        totales = [
            ["Subtotal", fmt(factura['subtotal'])],
            ["Descuento", fmt(factura['descuento'])],
            ["TOTAL", fmt(factura['total'])],
        ]
        tabla_totales = Table(totales, colWidths=[14 * cm, 3 * cm])
        tabla_totales.setStyle(TableStyle([
            ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 2), (-1, 2), ROJO_IDEAL),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ]))
        elementos.append(tabla_totales)
        elementos.append(Spacer(1, 1 * cm))
        elementos.append(Paragraph("Gracias por su compra.", normal))

        doc.build(elementos)
        buffer.seek(0)
        return buffer
