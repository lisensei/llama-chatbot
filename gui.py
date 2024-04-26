import streamlit as st
import langchain
from langchain_core.prompts import PromptTemplate
from model import get_model
from PIL import Image
import requests
langchain.debug=True
st.title("Sky Net")
st.session_state.character="SkyNet"

if "messages" not in st.session_state:
    st.session_state["messages"]=[]
    #msg=f"I am {st.session_state.character}, ask me any questions."
    #st.session_state.messages.append({"role":"assistant","content":msg})

for m in st.session_state.messages:
    if m["role"]=="user":
        with st.chat_message("user"):
            st.write(m["content"])
    if m["role"]=="assistant":
        with st.chat_message("assistant",avatar=Image.open("assets/umbrella_corporation.png")):
            st.write(m["content"])

prompt=st.chat_input("Type a message here...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("assistant",avatar=Image.open("assets/umbrella_corporation.png")):
        #format prompt according to the model's prompt format
        messages='''<s>[INST]You are Sky Net developed by the umbrella corporation, so behave accordingly.[/INST]'''
        for m in st.session_state.messages:
            if m["role"]=="user":
                messages+=f"[INST]{m['content']}[/INST]\n"
            else:
                messages+=f"{m['content']} </s>\n"
        #url of the flask api
        url="http://127.0.0.1:5000/stream/v1"
        out=requests.get(url,json={"messages":messages},stream=True)
        def stream_gen(data):
            for bs in data:
                yield bs.decode()
        response=st.write_stream(stream_gen(out))
    st.session_state.messages.append({"role":"assistant","content":response})