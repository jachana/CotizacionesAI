from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

def generate_quote_pdf(products, filename="quote.pdf"):
    pdf_file ="output/"+ filename
    #make sure the directory exists
    if not os.path.exists("output"):
        os.makedirs("output")

    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    table_data = [["Producto", "precio Unidad", "cantidad", "Total"]]

    # Add product data to table
    total_sum = 0
    for product in products:
        table_data.append([str(item) for item in product])
        total_sum += product[3]  # Accumulate total amount

    # Add final total row
    table_data.append(["Final", "", "", total_sum])

    # Create table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
     # Alternate row colors
    for index in range(1, len(table_data)):
        if index % 2 == 0:
            style.add('BACKGROUND', (0, index), (-1, index), colors.lightblue)
    # make the last row bold and in a bigger font and with a different background color
    style.add('BACKGROUND', (0, -1), (-1, -1), colors.white)

    style.add('TEXTCOLOR', (0, -1), (-1, -1), colors.black)
    style.add('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
    style.add('FONTSIZE', (0, -1), (-1, -1), 14)
    style.add('ALIGN', (0, -1), (-1, -1), 'CENTER')
    style.add('BOTTOMPADDING', (0, -1), (-1, -1), 12)

    # Create table
    table = Table(table_data)
    table.setStyle(style)

    # Add table to document
    doc.build([table])
    return doc

# input_data = [('Aceite LUBRAX HYDRA XP 46 T.208L', 427397, 2, 854794), ('Tellus S2 MX 46 208,1L', 686455, 2, 1372910), ('TOTAL AZOLLA ZS 46, 208L, CL', 593640, 2, 1187280), ('MOBIL DTE 26, 1040LT', 2768454, 2, 5536908)]

# generate_quote_pdf(input_data)
