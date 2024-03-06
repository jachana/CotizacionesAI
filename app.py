from openai import OpenAI
import streamlit as st
import main

st.title("Conico Cotizador de productos")

client = OpenAI()
# get the api key from the environment variable
client.api_key = st.secrets["OPENAI_API_KEY"]

#only do this once
if "products" not in st.session_state:
    with st.spinner(text="Cargando datos..."):
        main.load_data()
        st.session_state["products"] = "done"
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
st.markdown("test")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Que productos quiere cotizar"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(text="cotizando..."):
            response = main.find_alternatives(prompt)
        st.markdown(response)
        # wait for the assistant to respond
        

    st.session_state.messages.append({"role": "assistant", "content": response})
if st.button("Reset", type="primary"):
    del st.session_state.messages
    st.markdown("reseting")
    st.write("writing")
    st.rerun()
