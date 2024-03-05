# Import necessary libraries
import getProductsTable
import assistant_updater
import update_assistant_files
import fuzzy_search
import extract_products


def find_alternatives(message, amount):
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

        cotizacion.append((product_name, unit_price, total_price))
        print("\n")
    total = 0
    for product in cotizacion:
        total += product[2]
    print("Cotizacion: " + str(cotizacion))
    print("Total: " + str(total))

def test_extract_products():
    test_messages = ["necesito 5 tambores de nuto 68", "cotiza 2 baldes de morbilux ep 0",  "2 tambores de 5w30" , " 3 tambores de 20w50 y dos cajas de turbo 40", "cotiza 4 baldes de mobiltherm","cotizame un tambor de 20w50 lubrax","dos tambores de hydra xp 46 , 2 de tellus mx 46, 2 de azolla 46 y dos dte 26","una grasa de mobilux ep 2 y una grasa lubrax lith ep 2 en baldes" ]

    for message in test_messages:
        find_alternatives(message,5)
        print("\n\n")

#file_names = getProductsTable.create_data_files()
file_names = ["tambores.json", "baldes.json", "cajas.json", "otros.json"]
assistant_id_beta = "asst_LbmJPRklqR6vRttFUAlyNihU"
assistant_id = "asst_DCRo8rnaW5BEFToSLmGmW4x6"
#assistant_updater.update_assistant(assistant_id)


test_extract_products()

#update_assistant_files.remove_all_files()

#update_assistant_files.replace_all_files([assistant_id_beta,assistant_id], file_names)
#update_assistant_files.replace_all_files([assistant_id_beta,assistant_id], file_names)
