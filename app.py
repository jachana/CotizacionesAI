from openai import OpenAI
import streamlit as st
import main
import quote_to_pdf
from pathlib import Path
import os
import glob

st.title("Conico Cotizador de productos")

client = OpenAI()
# get the api key from the environment variable
client.api_key = st.secrets["OPENAI_API_KEY"]

def create_pdf(detail, quote_file_name):
    return quote_to_pdf.generate_quote_pdf(detail, quote_file_name)

def add_quote_button(detail, index):
    quote_file_name = "quote_" + str(index) + ".pdf"
    create_pdf(detail, quote_file_name)
    file_name = "output/" + quote_file_name
    file_data = Path(file_name).read_bytes()
    st.download_button("Descargar Cotizacion",file_data, quote_file_name)

def delete_output_files():
    files_to_delete = glob.glob('output/*')
    for deletable in files_to_delete:
        os.remove(deletable)
def setup_app():
    if "products" not in st.session_state:
        with st.spinner(text="Cargando datos..."):
            main.load_data()
            st.session_state["products"] = "done"
            delete_output_files()
    # create the messages list
    if "messages" not in st.session_state:
        st.session_state.messages = []
def run_app():
#create once in the session state objects
#create/overwrite products files with the latest data
    setup_app()

    message_index = 0
    for message in st.session_state.messages:
        message_index += 1
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        if message["role"] == "assistant":
            add_quote_button(message["quote"], message_index)

    if prompt := st.chat_input("Que productos quiere cotizar"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(text="cotizando..."):
                markdown, detail, _ = main.find_alternatives(prompt)
            st.markdown(markdown)
        add_quote_button(detail,message_index+2)
        st.session_state.messages.append({"role": "assistant", "content": markdown, "quote": detail})

    if len(st.session_state.messages)>0:
        if st.button("Reset", type="primary"):
            del st.session_state.messages
            del st.session_state.products
            st.rerun()
run_app()
