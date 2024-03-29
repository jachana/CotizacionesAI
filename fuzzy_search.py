import os
import fuzzywuzzy
import re
import json

from fuzzywuzzy import process
from fuzzywuzzy import fuzz


def custom_score(query, candidate):
    # Extract numbers from strings
    query_numbers = re.findall(r'\d+', query)
    candidate_numbers = re.findall(r'\d+', candidate)

    # Calculate base score using token sort ratio
    base_score = fuzz.token_sort_ratio(query, candidate)

    # Calculate numeric score if both strings contain numbers
    numeric_score = 0
    if query_numbers and candidate_numbers:
        # Simple example: compare the first number found in each string
        numeric_score = 100 - abs(int(query_numbers[0]) - int(candidate_numbers[0]))

    # Weighted sum of base score and numeric score
    # Adjust weights as needed
    final_score = 0.7 * base_score + 0.3 * numeric_score
    return final_score


def search_proper_name(query, product_format, viscosity=None, brand=None, product_type=None):

    #first determine which file to open
    files_to_open = []
    product_format = product_format.lower()
    if product_format == "tambor":
        files_to_open.append("tambores.json")
    elif product_format == "balde":
        files_to_open.append("baldes.json")
    elif product_format == "caja":
        files_to_open.append("cajas.json")
    else:
        files_to_open.append("tambores.json")
        files_to_open.append("baldes.json")
        files_to_open.append("cajas.json")
        files_to_open.append("otros.json")

    #now get all the products
    products = []
    product_names = []
    print("buscando en " + str(files_to_open))


    for file_name in files_to_open:
        file = open(file_name, "r")

        products_json_string = file.read()
        products_json = json.loads(products_json_string)

        product_names+= [product['Nombre'] for product in products_json]
        #add all the products to the list as an array
        products += [(product['Nombre'], product['Precio'], product['Marca'], product['Formato'], product['Tipo']) for product in products_json]

    #filter the products by viscosity  and brand if needed
    if viscosity:
        products = [product for product in products if product[4] == viscosity]
    if brand:
        products = [product for product in products if product[2] == brand]
    if product_type:
        products = [product for product in products if product[5] == product_type]

    #remove from the product names the ones that are not in the products list
    product_names = [product for product in product_names if product in [product[0] for product in products]]

    scores = [(product, custom_score(query, product)) for product in product_names]
    #print(scores)
    best_match = max(scores, key=lambda x: x[1])

    #get the best 3 scores
    scores_to_get = min(3, len(scores))
    best_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:scores_to_get]


    #find the best match on the products using the name
    best_product_match = None
    for product in products:
        if product[0] == best_match[0]:
            best_product_match = product
            break

    # for product, score in best_scores:
    #     print(f"{product} with a score of {score}")

    print (f"Best match: {best_product_match} with a score of {best_match[1]}")
    return best_product_match
