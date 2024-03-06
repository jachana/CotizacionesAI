import openai
import os
import json

from openai import OpenAI
client = OpenAI()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_products(messages):
    input_messages=[ {"role": "system", "content": "Eres un asistente que convierte solicitudes de productos en un formato estructurado. El formato sera un JSON con el nombre de los productos , el formato y la cantidad de cada uno. Por ejemplo, si la solicitud es 'necesito 5 tambores de nuto 68', el formato estructurado seria {'products': [{'product': 'nuto 68','format': 'tambor', 'quantity': 5}]}. Los posibles formatos son Balde, Tambor, Caja o desconosido"}      ]

    input_messages.extend([{"role": "user", "content": message} for message in messages])

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={"type":"json_object"},
    messages=input_messages
    )

    # create a dictionary to store the products and quantities with structure string : int
    products = {}

    # loop through the messages and extract the products and quantities
    response_content = completion.choices[0].message.content

    #parse the json response
    response_content = response_content.replace("'", "\"")
    response_content = json.loads(response_content)

    products = response_content['products']
    #response_content = json.loads(response_content)

    # for product in response_content['products']:
    #     products[product['product']] = product['quantity']

    return products





