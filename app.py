from openai import OpenAI
import streamlit as st
import main

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

def create_pdf(detail, total):
    print("Creating PDF")
    print(detail)

#unecessary?
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"


# print all the existing messages
message_index = 0
for message in st.session_state.messages:
    message_index += 1
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    if(message["role"] == "assistant"):
        if st.button("Enviar Cotizacion", type="primary", key=("send_quote" + str(message_index))):
            create_pdf(message["quote"], message["total"])
            st.markdown("cotizacion enviada")

if prompt := st.chat_input("Que productos quiere cotizar"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(text="cotizando..."):
            markdown, detail, total = main.find_alternatives(prompt)
        st.markdown(markdown)
        # wait for the assistant to respond


    st.session_state.messages.append({"role": "assistant", "content": markdown, "quote": detail, "total": total})
if len(st.session_state.messages)>0:
    if st.button("Reset", type="primary"):
        del st.session_state.messages
        del st.session_state.products
        st.rerun()

