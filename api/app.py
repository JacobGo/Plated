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
 

from flask import Flask, jsonify
app = Flask(__name__)

restaurants = [
   {'name' : session.query(Restaurant).first().name }
]

@app.route('/api/restaurants', methods=['GET'])
def get_tasks():
    return jsonify({'restaurants': restaurants})

if __name__ == '__main__':
    app.run(debug=True)