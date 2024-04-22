import streamlit as st
import langchain
from langchain_community.llms import LlamaCpp
from langchain_core.prompts import PromptTemplate
langchain.debug=True
llm=LlamaCpp(model_path="../llama/llama",n_gpu_layers=-1,n_ctx=4096)
character="SkyNet"
st.title("Llama Cpp Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"]=[]
    msg=f"I am {character}, ask any questions."
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
    temp='''[INST]<<SYS>>You are SkyNet.{context}<</SYS>>{messages}[/INST]'''
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("assistant"):
        messages=""
        for m in st.session_state.messages:
            if m["role"]=="user":
                messages+="user: "+m["content"]+"\n"
            else:
                messages+=f"{character}: "+m["content"]+"\n"
        template=PromptTemplate.from_template(temp)
        chain=template|llm
        out=chain.stream({"context":"","messages":messages})
        response=st.write_stream(out)
    st.session_state.messages.append({"role":"assistant","content":response})