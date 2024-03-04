# Import necessary libraries
import getProductsTable
import assistant_updater
import update_assistant_files
import fuzzy_search
import extract_products

#file_names = getProductsTable.create_data_files()
file_names = ["tambores.json", "baldes.json", "cajas.json", "otros.json"]
assistant_id_beta = "asst_LbmJPRklqR6vRttFUAlyNihU"
assistant_id = "asst_DCRo8rnaW5BEFToSLmGmW4x6"
#assistant_updater.update_assistant(assistant_id)


def find_best_match(message):
    products = extract_products.extract_products([message])
    print(products)
    for product in products:
        product_base_name = product['product']
        
        product_name = fuzzy_search.search_proper_name(product_base_name)

def find_alternatives(message, amount):
    products = extract_products.extract_products([message])
    print(message)
    print("---")

    for product in products:
        product_base_name = product['product']
        product_format = product['format']
        print(product_base_name)
        print("format: " + product_format)
        product_name = fuzzy_search.search_alternatives(product_base_name, product_format, amount)
        print("\n")
        
def test_extract_products():
    test_messages = ["necesito 5 tambores de nuto 68", "cotiza 2 baldes de morbilux ep 0",  "2 tambores de 5w30" , " 3 tambores de 20w50 y dos cajas de turbo 40" ]

    for message in test_messages:
        find_alternatives(message,5)
        print("\n\n")


test_extract_products()

#update_assistant_files.remove_all_files()

#update_assistant_files.replace_all_files([assistant_id_beta,assistant_id], file_names)
#update_assistant_files.replace_all_files([assistant_id_beta,assistant_id], file_names)
