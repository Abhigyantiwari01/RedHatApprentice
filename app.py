from flask import Flask, request,jsonify,Response
import pymongo 
from dotenv import load_dotenv
import os
from database import get_database
import uuid


load_dotenv()
print(os.environ["MONGO_URL"])
myclient = pymongo.MongoClient(os.environ["MONGO_URL"])
mydb = myclient["mydatabase"]
app = Flask(__name__)
db = get_database()
orderCollection = db["orders"]

@app.route("/welcome",methods=["GET"])
def welcome():
    return "Welcome to Pizza House"

@app.route("/order", methods=["POST"])
def order():
    print("running")
    body = request.json
    uniqueId = str(uuid.uuid4()).split("-")[0]
    orderObject = {
        "orderId":uniqueId,
        "content":body["order"]
    }
    print(orderObject)
    orderCollection.insert_one(orderObject)
    return jsonify({"orderId":uniqueId})

@app.route("/getorders", methods=["GET"])
def getOrder():
    orders = orderCollection.find()
    result = list(map(lambda order:{"orderId": order["orderId"],"content": order["content"]}, orders))
    return jsonify(result)

@app.route("/getorders/<order_id>", methods=["GET"])
def getOrderById(order_id):
    orders = orderCollection.find({"orderId":order_id})
    result = list(map(lambda order:{"orderId": order["orderId"],"content": order["content"]}, orders))
    if not result:
        return Response(status=404)
    return jsonify(result)




@app.route("/",methods=["GET"])
def heartbeat():
    return jsonify({"heartbeat":True})



