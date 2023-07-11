from flask import Flask, request, jsonify
import json
from bson import json_util, ObjectId
from datetime import datetime

# from db import DB
from pymongo import MongoClient, collection
class DB:
    def __init__(self,collection_name):
        self.client = MongoClient('mongodb+srv://mahendragurunathan:cvLfE7KpsawkA8op@inventory.2i0b34n.mongodb.net/')
        self.db = self.client.get_database('store')
        self.collection = collection.Collection(self.db, collection_name)
app = Flask(__name__)


@app.route('/item', methods=['POST'])
def post_item():
    db = DB('inventory')
    item = request.get_json()
    item_name = item["item_name"]
    item_quantity = item["item_quantity"]
    item_category = item["item_category"]
    response = db.collection.insert_one(item)
    return jsonify("Item added Successfully")

@app.route('/items')
def get_items():
    db=DB('inventory')
    response = db.collection.find()
    response = json.loads(json_util.dumps(response))
    return jsonify(response)

@app.route('/items', methods=['POST'])
def post_items():
    db = DB('items')
    item = request.get_json()
    customer_name = item["customer_name"]
    customer_contact = item["customer_contact"]
    invoice_no = item["invoice_no"]
    items = item["items"]
    period = datetime.now().isoformat()
    bill = item["bill"]
    item["period"] = period
    response = db.collection.insert_one(item)
    return jsonify("Item added Successfully")


@app.route('/items', methods=['DELETE'])
def delete_items():
    db = DB('items')
    id = request.args.get('id')
    item_id = request.args.get('item_id')
    items = db.collection.find_one(ObjectId(id))
    item = items["items"]
    data = []
    for x in item:
        if x["_id"]["$oid"] in item_id:
            pass
        else:
            data.append(x)

    # items["items"] = data

    print(items)
    # return jsonify(items)
#     print(item["_id"]["$oid"])
#     item_id = item["_id"]["$oid"]
#     items = item["items"]
    payload = dict()
    payload["items"] = data
    print(payload)
    response = db.collection.update_one({ "_id": ObjectId(id) },{
    "$set": payload
   })
    return jsonify("Item deleted Successfully")


@app.route('/invoices')
def get_invoices():
    db = DB('items')
    response = db.collection.find()
    response = json.loads(json_util.dumps(response))
    return jsonify(response)


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)