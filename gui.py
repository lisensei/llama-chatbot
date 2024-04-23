import streamlit as st
import langchain
from langchain_core.prompts import PromptTemplate
from model import get_model
langchain.debug=True
st.title("Llama Cpp Chatbot")
st.session_state.character="SkyNet"

if "model" not in st.session_state:
    #fill in the correct path to the a llama cpp model
    st.session_state.model=get_model()

if "messages" not in st.session_state:
    st.session_state["messages"]=[]
    msg=f"I am {st.session_state.character}, ask any questions."
    st.session_state.messages.append({"role":"assistant","content":msg})

for m in st.session_state.messages:
    if m["role"]=="user":
        with st.chat_message("user"):
            st.write(m["content"])
    if m["role"]=="assistant":
        with st.chat_message("assistant"):
            st.write(m["content"])

prompt=st.chat_input("Type a message here...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("assistant"):
        #format prompt according to the model's prompt format
        temp='''<s>{messages}'''
        messages=""
        for m in st.session_state.messages:
            if m["role"]=="user":
                messages+=f"[INST]{m['content']}[/INST]\n"
            else:
                messages+=f"{m['content']} </s>\n"
        template=PromptTemplate.from_template(temp)
        chain=template|st.session_state.model
        out=chain.stream({"context":"","messages":messages})
        response=st.write_stream(out)
    st.session_state.messages.append({"role":"assistant","content":response})