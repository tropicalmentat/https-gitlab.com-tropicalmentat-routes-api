# https://dev.to/andrewbaisden/creating-react-flask-apps-that-connect-to-postgresql-and-harperdb-1op0
import flask
from sqlalchemy import create_engine
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv


DATABASE = os.getenv('DATABASE')
HOSTNAME = os.getenv('HOSTNAME')
PORT = os.getenv('PORT')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

app = flask.Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

try:
    con = psycopg2.connect(
    	host=HOSTNAME,
    	port=PORT,
        database=DATABASE,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD)

    cur = con.cursor()

    @app.route('/')
    def fetch_all_bike_parking():
        cur.execute("SELECT *,ST_X(ST_Transform(geom,4326)) as long,ST_Y(ST_Transform(geom,4326)) as lat FROM traffic where fclass='parking_bicycle'")
        rows = cur.fetchall()

        return flask.jsonify(rows)

except Exception as e:
	print(e)