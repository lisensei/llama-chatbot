from flask import Flask,request,jsonify
from model import get_model
from langchain_core.prompts import PromptTemplate
import json
from argparse import ArgumentParser
import langchain
langchain.debug=True
parser=ArgumentParser()
parser.add_argument("-model_path",type=str)
app=Flask(__name__)
app.config["MODEL_PATH"]=""
@app.route("/conversation/v1",methods=["POST"])
def conversation():
    messages=json.loads(request.data.decode())["messages"]
    model=get_model(app.config["MODEL_PATH"])
    temp='''{messages}'''
    template=PromptTemplate.from_template(temp)
    chain=template|model
    response=chain.invoke({"messages":messages})
    return jsonify({"response:":response})

@app.route("/stream/v1",methods=["GET"])
def stream():
    messages=json.loads(request.data.decode())["messages"]
    model=get_model(app.config["MODEL_PATH"])
    temp='''{messages}'''
    template=PromptTemplate.from_template(temp)
    chain=template|model
    response=chain.stream({"messages":messages})
    return response
if __name__=="__main__":
    args=parser.parse_args()
    app.config["MODEL_PATH"]=args.model_path
    app.run(debug=True)