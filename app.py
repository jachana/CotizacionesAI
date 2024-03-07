from openai import OpenAI
import streamlit as st
import main
import quote_to_pdf
from pathlib import Path

st.title("Conico Cotizador de productos")

client = OpenAI()
# get the api key from the environment variable
client.api_key = st.secrets["OPENAI_API_KEY"]

#create once in the session state objects
#create/overwrite products files with the latest data
if "products" not in st.session_state:
    with st.spinner(text="Cargando datos..."):
        main.load_data()
        st.session_state["products"] = "done"
# create the messages list
if "messages" not in st.session_state:
    st.session_state.messages = []

def create_pdf(detail, quote_file_name):
    return quote_to_pdf.generate_quote_pdf(detail, quote_file_name)

def add_quote_button(detail, total, index):
    #if st.button("Crear Cotizacion", type="primary", key=("send_quote" + str(index))):
        quote_file_name = "quote_" + str(index) + ".pdf"
        create_pdf(detail, quote_file_name)
        #st.markdown(detail)
        file_name = "output/" + quote_file_name
        file_data = Path(file_name).read_bytes()
        st.download_button("Descargar Cotizacion",file_data, quote_file_name)
#unecessary?
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"


message_index = 0
for message in st.session_state.messages:
    message_index += 1
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if(message["role"] == "assistant"):
        add_quote_button(message["quote"], message["total"], message_index)

if prompt := st.chat_input("Que productos quiere cotizar"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(text="cotizando..."):
            markdown, detail, total = main.find_alternatives(prompt)
        st.markdown(markdown)
    add_quote_button(detail,total,message_index+2)
        # wait for the assistant to respond


    st.session_state.messages.append({"role": "assistant", "content": markdown, "quote": detail, "total": total})
if len(st.session_state.messages)>0:
    if st.button("Reset", type="primary"):
        del st.session_state.messages
        del st.session_state.products
        st.rerun()
