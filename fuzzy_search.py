import os
import fuzzywuzzy
import re

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

def search_proper_name(query):
    #open the file
    file = open("tambores.csv", "r")
    products = []

    for line in file:
        split_line = line.split(";")
        products.append(split_line[0])
    # The search query

    # def test():

    #     # Find the best match for the query in the list of products
    #     best_match = process.extractOne(query, products)

    #     print(f"Best match for '{query}': {best_match[0]} with a score of {best_match[1]}")

    #     # Find the top 3 matches for the query
    #     matches = process.extract(query, products, limit=30)

    #     print(f"Top matches for '{query}':")
    #     for match in matches:
    #         print(f"{match[0]} with a score of {match[1]}")

    scores = [(product, custom_score(query, product)) for product in products]
    best_match = max(scores, key=lambda x: x[1])

    #get the best 30 scores
    best_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:30]

    for product, score in best_scores:
        #print(f"{product} with a score of {score}")
        pass
    print(f"Best match for '{query}': {best_match[0]} with a score of {best_match[1]}")
    return best_match[0]

def search_alternatives(query, amount):
    file = open("tambores.csv", "r")
    products = []

    for line in file:
        split_line = line.split(";")
        products.append(split_line[0])
    # The search query

    # def test():

    #     # Find the best match for the query in the list of products
    #     best_match = process.extractOne(query, products)

    #     print(f"Best match for '{query}': {best_match[0]} with a score of {best_match[1]}")

    #     # Find the top 3 matches for the query
    #     matches = process.extract(query, products, limit=30)

    #     print(f"Top matches for '{query}':")
    #     for match in matches:
    #         print(f"{match[0]} with a score of {match[1]}")

    scores = [(product, custom_score(query, product)) for product in products]
    best_match = max(scores, key=lambda x: x[1])

    #get the best 30 scores
    best_scores = sorted(scores, key=lambda x: x[1], reverse=True)[:30]

    for product, score in best_scores:
        #print(f"{product} with a score of {score}")
        pass
    print(f"Best match for '{query}': {best_match[0]} with a score of {best_match[1]}")
    return best_match[:amount]
