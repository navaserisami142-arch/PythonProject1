from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def render_invoice(order):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>Sam Store Invoice</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Order Number : {order.id}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Customer : {order.first_name} {order.last_name}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Email : {order.email}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Phone : {order.phone}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Address : {order.address}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    data = [
        [
            "Product",
            "Qty",
            "Price",
            "Total",
        ]
    ]

    for item in order.items.all():

        data.append(
            [
                item.product.name,
                item.quantity,
                f"${item.price}",
                f"${item.get_total_price()}",
            ]
        )

    table = Table(data)

    table.setStyle(

        TableStyle(

            [

                ("BACKGROUND", (0, 0), (-1, 0), colors.indigo),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.grey),

                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

            ]

        )

    )

    elements.append(table)

    elements.append(Spacer(1, 25))

    elements.append(

        Paragraph(

            f"<b>Total : ${order.get_total_price()}</b>",

            styles["Heading2"]

        )

    )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf