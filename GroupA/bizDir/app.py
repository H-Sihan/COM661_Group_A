# pip install flask, requests
# pip install pymongo

from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.Biz_Database
businesses = db.biz

@app.route('/', methods=['GET'])
def home():
    return make_response(jsonify({"message":"Welcome to Flask"}), 200)

# Get all businesses from MongoDB
@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    data_to_return = []
    
    page_num = request.args.get('pn', default=1, type=int)
    page_size = request.args.get('ps',default=3, type=int)
    page_start = (page_num - 1) * page_size

    try:
        businesses_cursor = businesses.find().skip(page_start).limit(page_size)
        
        for business in businesses_cursor:
            business['_id'] = str(business['_id'])
            
           # for review in business.get('reviews', []):
            #    review['_id'] = str(review['_id'])
            
            data_to_return.append(business)
        
        return make_response(jsonify(data_to_return), 200)
    
    except ConnectionError:
        return make_response(jsonify({"error":"Database not connected"}),500)
    
    except Exception as ex:
        return make_response(jsonify({"Error":"Internal server","details":str(ex)}),500)    
# ------------------------------------------------------------------------------------------------------
# Get one business from MongoDB ==== 699c42eaa797528ab5db5821
@app.route('/api/businesses/<string:biz_id>', methods=['GET'])
def get_one_busines(biz_id):
    
    biz = businesses.find_one({"_id":ObjectId(biz_id)})
    if biz is not None:
        biz['_id'] = str(biz['_id'])
        
        for review in biz["reviews"]:
            review["_id"] = str(review["_id"])
        
        return make_response(jsonify(biz), 200)
    
    else:
        return make_response(jsonify({"Error":"Business not found"}),404)    

# ------------------------------------------------------------------------------------------------------
@app.route('/api/businesses', methods=['POST'])
def add_business():
    data = request.form
    next_id = businesses[-1]["id"] + 1

    new_business = {
        "id":next_id,
        "name":data.get("name"),
        "town":data.get("town"),
        "rating":int(data.get("rating", 0)),
        "reviews":[]
    }
    businesses.append(new_business)
    return make_response(jsonify({"New business": new_business}), 201)
    
if __name__ == '__main__':
    app.run(debug= True, port=5001)
    
