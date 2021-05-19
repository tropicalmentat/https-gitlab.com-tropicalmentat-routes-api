# https://dev.to/andrewbaisden/creating-react-flask-apps-that-connect-to-postgresql-and-harperdb-1op0
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
import requests


DATABASE = os.getenv('DATABASE')
HOSTNAME = os.getenv('HOSTNAME')
PORT = os.getenv('PORT')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
GRAPHHOPPER_IP=os.getenv('GRAPHHOPPER_IP')

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

try:
    #@app.route('/')
    #def index():
    #    '''Index page route'''

    #    return '<h1>TEST ROWT API<h1>'


    con = psycopg2.connect(
    	host=HOSTNAME,
    	port=PORT,
        database=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD)

    cur = con.cursor()

    @app.route('/get-bike-parking')
    def fetch_all_bike_parking():
        coords = request.args.getlist('point')
        destination = coords[1].split(',')
        #destination = '14.55094,121.04971'
        cur.execute(f"select osm_id,ST_Y(ST_Transform(geom,4326))as lat,ST_X(ST_Transform(geom,4326)) as lng from (select osm_id,way as geom, ST_Contains(ST_Buffer(ST_Transform(ST_SetSRID(ST_Point({destination[1]},{destination[0]}),4326),32651),200),ST_Transform(way,32651)) as result from planet_osm_point where tags->'amenity'='bicycle_parking') as res where result='t';")

        rows = cur.fetchall()

        return jsonify(rows)
        

    @app.route('/route')
    def fetch_route():
        coords = request.args.getlist('point')
        origin = coords[0]
        destination = coords[1]
        r = requests.get(f'http://{GRAPHHOPPER_IP}/route?point={origin}&point={destination}&points_encoded=false')

        return r.text

except Exception as e:
	print(e)

if __name__ == '__main__':
    app.run()
