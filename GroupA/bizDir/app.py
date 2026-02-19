# pip install flask, requests

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

businesses = [
    {
        "id":1,
        "name":"Costa",
        "town":"London",
        "rating":5,
        "reviews":[]
    },
    {
        "id":2,
        "name":"Nero",
        "town":"London",
        "rating":4,
        "reviews":[]
    },
      {
        "id":3,
        "name":"Pret",
        "town":"London",
        "rating":5,
        "reviews":[]
    }
]

@app.route('/', methods=['GET'])
def home():
    return make_response(jsonify({"message":"Welcome to Flask"}), 200)

@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    return make_response(jsonify({"Businesses":businesses}))

@app.route('/api/businesses/<int:biz_id>', methods=['GET'])
def get_one_busines(biz_id):
    for biz in businesses:
        if biz['id'] == biz_id:
            return make_response(jsonify(biz), 200)
    
    return make_response(jsonify({"Error":"No Business found"}), 404)

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
    app.run(debug= True)
    
