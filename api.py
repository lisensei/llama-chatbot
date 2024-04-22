from flask import Flask,request,jsonify
from model import get_model
from langchain_core.prompts import PromptTemplate
import json
app=Flask(__name__)

@app.route("/conversation/v1",methods=["POST"])
def conversation():
    messages=json.loads(request.data.decode())["messages"]
    model=get_model()
    temp='''<s>[INST]You are an AGI that knows everything, answer questions in a concise manner. {messages}[/INST]'''
    template=PromptTemplate.from_template(temp)
    chain=template|model
    response=chain.invoke({"messages":messages})
    return jsonify({"response:":response})
if __name__=="__main__":
    app.run(debug=True)