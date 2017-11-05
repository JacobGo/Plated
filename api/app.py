from flask import Flask, jsonify, make_response, abort, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from flask_cors import CORS
from pprint import pprint

from yelpapi import YelpAPI
from keys import Keys
yelp_api = YelpAPI(Keys()._id, Keys().secret)
la = 42.39
lo = -72.52
# pprint(yelp_api.search_query(longitude=lo,latitude=la))

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db/plated.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=True)
    type = db.Column(db.String(250), nullable=True) #Chinese, cafe, fast food...
    popularity = db.Column(db.Float, nullable=True)
    recommendation = db.Column(db.Float, nullable=True) #dict {user_id : float}
class RestaurantSchema(Schema):
    class Meta:
        fields = ['id','name','type','popularity', 'recommendation']
restaurant_schema = RestaurantSchema()

# new_restaurant = Restaurant(name='Not Antonio\'s', popularity=-1.0, type='Chinese', recommendation=0.0)
# db.session.add(new_restaurant)
# db.session.commit()


@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    return jsonify([restaurant_schema.dump(restaurant) for restaurant in Restaurant.query.all()])


@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    #q = 'SELECT '
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()#[r for r in restaurants if restaurants.id == restaurant_id]
    if not (restaurant): #== 0:
        abort(404)
    return jsonify(restaurant_schema.dump(restaurant))

@app.route('/api/restaurants/like', methods=['POST'])
def like_restaurant():
    if not request.form:
        abort(400)
    restaurant_id = request.form['id']
    liked = request.form['like']
    # if not restaurant_id or not liked:
    #     abort(400)
    # if liked < -1 or liked > 1:
    #     abort(400)
    restaurant = Restaurant.query.filter(Restaurant.id == restaurant_id).first()
    # if not restaurant:
    #     abort(400)
        
    restaurant.popularity += int(liked);
    db.session.commit()

    return jsonify(restaurant_schema.dump(restaurant)), 201

def create_restaurant(json_data):
    r = Restaurant(name=json_data['name'],
                   popularity=json_data['popularity'],
                   type=json_data['type'],
                   recommendation=json_data['recommendation'])
    db.session.add(r)
    db.session.commit()
    return r
@app.route('/api/restaurants', methods=['POST'])
def add_restaurant():
    if not request.json:
        abort(400)
    restaurant = create_restaurant(request.json)
    return jsonify(restaurant_schema.dump(restaurant)), 201


# @app.route('/api/restaurants/<int:restaurant_id>', methods=['PUT'])
# def update_restaurant(restaurant_id):
#     restaurant = [restaurant for restaurant in restaurants if restaurant['id'] == restaurant_id]
#     if len(restaurant) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     """if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)"""
#     restaurant[0]['title'] = request.json.get('title', restaurant[0]['title'])
#     restaurant[0]['description'] = request.json.get('description', restaurant[0]['description'])
#     restaurant[0]['done'] = request.json.get('done', restaurant[0]['done'])
#     return jsonify({'restaurant': restaurant[0]})
#
#
# @app.route('/api/restaurants<int:restaurant_id>', methods=['DELETE'])
# def delete_restaurant(restaurant_id):
#     restaurant = [restaurant for restaurant in restaurants if restaurant['id'] == restaurant_id]
#     if len(restaurant) == 0:
#         abort(404)
#     restaurants.remove(restaurant[0])
#     return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)