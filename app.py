from flask import Flask, request,jsonify,Response
import pymongo 
from dotenv import load_dotenv
import os
from database import get_database
import uuid
from messageQueue import enqueue,dequeue,initialize_queue,channel
import json
from threading import Thread
load_dotenv()
initialize_queue()
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
    """
    Heavy consmption tasks like database insertion are done inside the queue for load balancing
    The database task insertion can be changed into any other high computational function
    """
    print("running")
    body = request.json
    uniqueId = str(uuid.uuid4()).split("-")[0]
    orderObject = {
        "orderId":uniqueId,
        "content":body["order"]
    }
    print(orderObject)
    #pushing the order to message queue
    enqueue(json.dumps(orderObject))
    return jsonify({"orderId":uniqueId})

def old_nonbalanced_order():
    """
    This is the old endpoint function which was used inintially for non load balanced requests post
    """
    print("running")
    body = request.json
    uniqueId = str(uuid.uuid4()).split("-")[0]
    orderObject = {
        "orderId":uniqueId,
        "content":body["order"]
    }
    print(orderObject)
    #pushing the order to message queue
    orderCollection.insert_one(orderObject)
    return jsonify({"orderId":uniqueId})

def placeOrder(a,b,c,orderObject):
    
    print("DEQUEUED",orderObject)
    orderCollection.insert_one(json.loads(orderObject))
dequeue(placeOrder)

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


def startConsumption(): 
    channel.start_consuming()

thread = Thread(target=startConsumption)
thread.start()


