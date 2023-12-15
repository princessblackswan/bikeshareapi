from flask import Flask, request
import sqlite3
import requests
from tqdm import tqdm
import json 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__) 

# make connection
def make_connection():
    connection = sqlite3.connect('austin_bikeshare.db')
    return connection
conn = make_connection()

@app.route('/')
@app.route('/home/')
def home():
    return 'Hello World'

@app.route('/stations/')
def route_all_stations():
    conn = make_connection()
    stations = get_all_stations(conn)
    return stations.to_json()

@app.route('/stations/<station_id>')
def route_stations_id(station_id):
    conn = make_connection()
    station = get_station_id(station_id, conn)
    return station.to_json()

@app.route('/trips/')
def route_all_trips():
    conn = make_connection()
    trips = get_all_trips(conn)
    return trips.to_json()

@app.route('/trips/<trip_id>')
def route_trips_id(trip_id):
    conn = make_connection()
    trips = get_trip_id(trip_id, conn)
    return trips.to_json()

@app.route('/json/', methods=['POST']) 
def json_example():
    req = request.get_json(force=True) # Parse the incoming json data as Dictionary
    name = req['name']
    age = req['age']
    address = req['address']
    return (f'''Hello {name}, your age is {age}, and your address in {address}
            ''')

@app.route('/stations/add', methods=['POST']) 
def route_add_station():
    data = pd.Series(eval(request.get_json(force=True))) 
    data = tuple(data.fillna('').values)
    conn = make_connection()
    result = insert_into_stations(data, conn)
    return result

@app.route('/trips/add', methods=['POST']) 
def route_add_trips():
    data = pd.Series(eval(request.get_json(force=True))) 
    data = tuple(data.fillna('').values)
    conn = make_connection()
    result = insert_into_trips(data, conn)
    return result


@app.route('/trips/average_duration')
def trips_avg_duration():
    conn = make_connection()
    trips = get_all_trips(conn)
    table = avg_duration(trips)
    return table

@app.route('/trips/average_duration/<bike_id>')
def trips_bikeid(bike_id):
    conn = make_connection()
    bikeid = get_bike_id(bike_id, conn)
    return bikeid


@app.route('/aggregation', methods=['POST']) 
def input_time():
    req = request.get_json(force=True) 
    start = req['start']
    end = req['end']
    conn = make_connection()
    result = aggregate(start, end, conn)
    return result.to_json()


###### FUNCTIONS ######

def get_all_stations(conn):
    query = f"""SELECT * FROM stations"""
    result = pd.read_sql_query(query, conn)
    return result

def get_station_id(station_id, conn):
    query = f"""SELECT * FROM stations WHERE station_id = {station_id}"""
    result = pd.read_sql_query(query, conn)
    return result 

def get_all_trips(conn):
    query = f"""SELECT * FROM trips"""
    result = pd.read_sql_query(query, conn)
    return result

def get_trip_id(trip_id, conn):
    query = f"""SELECT * FROM trips WHERE id = {trip_id}"""
    result = pd.read_sql_query(query, conn)
    return result 

def insert_into_stations(data, conn):
    query = f"""INSERT INTO stations values {data}"""
    try:
        conn.execute(query)
    except:
        return 'Error'
    conn.commit()
    return 'OK'

def insert_into_trips(data, conn):
    query = f"""INSERT INTO trips values {data}"""
    try:
        conn.execute(query)
    except:
        return 'Error'
    conn.commit()
    return 'OK'


def avg_duration(trips):
    avg_dur = trips.groupby("subscriber_type")["duration_minutes"].mean().sort_values()
    return avg_dur.to_json()


def get_bike_id(bike_id, conn):
    query = f"""SELECT * FROM trips WHERE bikeid = {bike_id}"""
    result = pd.read_sql_query(query, conn)
    avg_dur = result.groupby("subscriber_type")["duration_minutes"].mean()
    return avg_dur.to_json()

def aggregate(start, end, conn):
    query = f"""SELECT t.*, s.station_id, s.name, s.status, s.address FROM trips AS t LEFT JOIN stations AS s ON t.start_station_id = s.station_id WHERE t.start_time BETWEEN '{start}' AND '{end}'"""
    result = pd.read_sql_query(query, conn)
    result = result.groupby('start_station_id').agg({
    'bikeid' : 'count', 
    'duration_minutes' : 'mean'})
    return result

if __name__ == '__main__':
    app.run(debug=True, port=5000)
