from flask import Flask, request,jsonify
import pymongo 
from dotenv import load_dotenv
import os

load_dotenv()
print(os.environ["MONGO_URL"])
myclient = pymongo.MongoClient(os.environ["MONGO_URL"])
mydb = myclient["mydatabase"]
app = Flask(__name__)

@app.route("/welcome",methods=["GET"])
def welcome():
    return "Welcome to Pizza House"


@app.route("/",methods=["GET"])
def heartbeat():
    return jsonify({"heartbeat":True})



