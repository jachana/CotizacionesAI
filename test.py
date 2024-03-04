import fuzzy_search
import extract_products

def test_extract_products():
    messages = ["necesito 5 tambores de nuto 68"]
    products = extract_products.extract_products(messages)

    for product in products:
        product = product['product']
        product_name = fuzzy_search.search_proper_name("nuto 68")
        print(product_name)

test_extract_products()
