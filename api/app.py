from flask import Flask, jsonify, make_response, abort, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('db')
from db.init import Base, Restaurant


engine = create_engine('sqlite:///plated.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
 
# Insert a Person in the person table
new_restaurant = Restaurant(name='Antonio\'s')
session.add(new_restaurant)
session.commit()

app = Flask(__name__)

restaurants = [
   {'name' : session.query(Restaurant).first().name }
]

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    return jsonify({'restaurants': restaurants})

@app.route('/api/restaurants', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = [r for r in restaurants if restaurants['id'] == restaurant_id]
    if len(restaurant) == 0:
        abort(404)
    return jsonify({'restaurant': restaurant[0]})

@app.route('/api/restaurants', methods=['POST'])
def create_restaurant():
    if not request.json or not 'title' in request.json:
        abort(400)
    restaurant = Restaurants("")
    restaurants.append(restaurant)
    return jsonify({'restaurant': restaurant}), 201

@app.route('/api/restaurants/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    restaurant = [restaurant for restaurant in restaurants if restaurant['id'] == restaurant_id]
    if len(restaurant) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    restaurant[0]['title'] = request.json.get('title', restaurant[0]['title'])
    restaurant[0]['description'] = request.json.get('description', restaurant[0]['description'])
    restaurant[0]['done'] = request.json.get('done', restaurant[0]['done'])
    return jsonify({'restaurant': restaurant[0]})

@app.route('/api/restaurants<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = [restaurant for restaurant in restaurants if restaurant['id'] == restaurant_id]
    if len(restaurant) == 0:
        abort(404)
    restaurants.remove(restaurant[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)