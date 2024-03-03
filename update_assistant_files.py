#this file is used to update the assistant with the latest data
#
 # Import necessary libraries
import openai
import requests
import os
from openai import OpenAI

# get OpenAI API Key from the environment
openai.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()


def upload_file(path):
    file_object = client.files.create(file=open(path, "rb"),purpose="assistants")

    return file_object.id

def remove_all_files():
    #first I need to get all the files
    all_files = client.files.list(purpose="assistants")
    #then I need to delete all the files
    for file in all_files:
        client.files.delete(file_id=file.id)
    print("All files deleted successfully")

def replace_all_files(assistant_ids, paths):
    #first I need to upload the files to openai
    file_ids = []
    old_file_ids = []

    for path in paths:
        file_ids.append(upload_file(path))
    for assistant_id in assistant_ids:
        # then I need to get the file ids assosiacted with the assistant
        assistant_files = client.beta.assistants.files.list(assistant_id=assistant_id)
        for file in assistant_files:
            old_file_ids.append(file.id)
        #cleanup repeated file ids
        old_file_ids = list(set(old_file_ids))

        #add the files to the assistant
        for file_id in file_ids:
            assistant_file = client.beta.assistants.files.create(assistant_id=assistant_id,file_id=file_id)

    #delete the old files
    for file_id in old_file_ids:
        deleted_assistant_file = client.beta.assistants.files.delete(assistant_id=assistant_id,file_id=file_id)
        client.files.delete(file_id=file_id)
    print ("Files replaced successfully")

    