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
#print(yelp_api.search_query(longitude=lo,latitude=la))

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
    return jsonify([restaurant_schema.dump(restaurant) for restaurant in Restaurant.query.order_by(Restaurant.popularity).all()])


@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
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
                   popularity = json_data['review_count'],
                   type=json_data['categories'][0]['title'],
                   recommendation=None)#json_data['recommendation'])
    db.session.add(r)
    db.session.commit()
    return r
@app.route('/api/restaurants', methods=['POST'])
def add_restaurant():
    if not request.json:
        abort(400)
    restaurant = create_restaurant(request.json)
    return jsonify(restaurant_schema.dump(restaurant)), 201

def clear_restaurants():
    Restaurant.query.delete()
    db.session.commit()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def get_search_parameters(lat, long):
    # See the Yelp API for more details
    params = {}
    #params["term"] = "restaurant"
    params["ll"] = "{},{}".format(str(lat), str(long))
    #params["radius_filter"] = "2000"
    #params["limit"] = "10"
    return params

#term = ''; location = 'austin, tx'; sort_by = 'rating', limit = 5
def get_results():
    # Obtain these from Yelp's manage access page
    la = 42.39
    lo = -72.52
    data = yelp_api.search_query(longitude=lo,latitude=la, sort_by = 'review_count', limit = 10, term = 'restaurant')
    add_to_db(data)
    return data

def add_to_db(results):
    for business in results["businesses"]:
        create_restaurant(business)
#clear_restaurants()
#get_results()

if __name__ == '__main__':
    app.run(debug=True)

