# Import necessary libraries
import getProductsTable
import assistant_updater
import update_assistant_files
import fuzzy_search
import extract_products
from flask import Flask, request, render_template

#file_names = getProductsTable.create_data_files()
file_names = ["tambores.json", "baldes.json", "cajas.json", "otros.json"]
assistant_id_beta = "asst_LbmJPRklqR6vRttFUAlyNihU"
assistant_id = "asst_DCRo8rnaW5BEFToSLmGmW4x6"


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.form['input_text']
    # Here, replace `process_text` with the name of your function that processes the text
    output_text, total_price = find_alternatives(input_text)
    #transform to html
    html_text = make_html(output_text, total_price)
    print(html_text)

    return render_template('result.html', output_text=html_text)

def process_text(text):
    return text.upper()

if __name__ == '__main__':
    app.run(debug=False)

def make_html(cotizacion, total):
    # Sample data in the specified format
    products = cotizacion

    # Start of the HTML table, defining the headers
    html_table = """
    <table border="1">
        <tr>
            <th>Product Name</th>
            <th>Unit Price</th>
            <th>Product Quantity</th>
            <th>Total Price</th>
        </tr>
    """

    # Adding each product's details to the table
    for product in products:
        html_table += f"""
        <tr>
            <td>{product[0]}</td>
            <td>{product[1]}</td>
            <td>{product[2]}</td>
            <td>{product[3]}</td>
        </tr>
        """
    html_table += f"""
        <tr>
            <td>Total</td>
            <td></td>
            <td></td>
            <td>{total}</td>
        </tr>
        """
    # Closing the table
    html_table += "</table>"

    print(html_table)
    return html_table


def find_alternatives(message):
    products = extract_products.extract_products([message])
    print(message)
    print("---")
    cotizacion = []
    for product in products:
        product_base_name = product['product']
        product_format = product['format']
        product_quantity = product['quantity']
        #get viscosity if it exists
        if 'viscosity' in product:
            product_viscosity = product['viscosity']
        else:
            product_viscosity = None
        if 'brand' in product:
            product_brand = product['brand']
        else:
            product_brand = None
        if 'type' in product:
            product_type = product['type']
        else:
            product_type = None
        print("producto: " + product_base_name)
        print("formato: " + product_format)
        print("cantidad: " + str(product_quantity))
        print("viscosidad: " + str(product_viscosity))
        print("marca: " + str(product_brand))
        print("tipo: " + str(product_type))

        product = fuzzy_search.search_proper_name(product_base_name, product_format, product_viscosity, product_brand, product_type)
        #print("best: " + str(product_name))
        product_name = product[0]
        unit_price = product[1]
        total_price = product_quantity * unit_price

        cotizacion.append((product_name, unit_price, product_quantity, total_price))
        print("\n")
    total = 0
    for product in cotizacion:
        total += product[3]
    print("Cotizacion: " + str(cotizacion))
    print("Total: " + str(total))
    return cotizacion, total

def test_extract_products():
    test_messages = ["necesito 5 tambores de nuto 68", "cotiza 2 baldes de morbilux ep 0",  "2 tambores de 5w30" , " 3 tambores de 20w50 y dos cajas de turbo 40", "cotiza 4 baldes de mobiltherm","cotizame un tambor de 20w50 lubrax","dos tambores de hydra xp 46 , 2 de tellus mx 46, 2 de azolla 46 y dos dte 26","una grasa de mobilux ep 2 y una grasa lubrax lith ep 2 en baldes" ]

    for message in test_messages:
        find_alternatives(message)
        print("\n\n")


#assistant_updater.update_assistant(assistant_id)


#test_extract_products()

#update_assistant_files.remove_all_files()

#update_assistant_files.replace_all_files([assistant_id_beta,assistant_id], file_names)
#update_assistant_files.replace_all_files([assistant_id_beta,assistant_id], file_names)
