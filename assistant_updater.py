# Import necessary libraries
import os
import openai
import requests
from openai import OpenAI

client = OpenAI()
# get OpenAI API Key from the environment
openai.api_key = os.getenv('OPENAI_API_KEY')


def update_assistant(assistant_id):
    # Update the assistant
    my_updated_assistant = client.beta.assistants.update(
      "asst_LbmJPRklqR6vRttFUAlyNihU",
      name="Cotizador de Productos",
      tools=[{"type": "retrieval"}],
      model="gpt-3.5-turbo-0125",
      file_ids=["file-3vmOAjeYUTlDaRRwIgyGsMb3", "file-4JGejDe3N90llgFnavpIT9aJ", "file-TY1o9qOi33YovegnPXqUkpo8", "file-slNlOAIq3mU9du94Du9DYhfi"],
    )

    print(my_updated_assistant)
