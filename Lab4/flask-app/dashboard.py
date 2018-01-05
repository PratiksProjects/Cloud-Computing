#!/usr/bin/env python
import flask
from flask import request, render_template, jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
import cPickle as pickle
import datetime
import time
import json
import sys

def avg(arr):
    return float(sum(arr)/len(arr))
# Create the application.
APP = flask.Flask(__name__)

#Enter AWS Credentials
AWS_ACCESS_KEY="" 
AWS_SECRET_KEY=""
REGION="us-east-1"


# Get the table
dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            region_name=REGION)

table = dynamodb.Table('SensorData')
#route for data between start and end dates, date format is YYYY-MM-DD
@APP.route('/getdata/<startDate>/<endDate>')
def get_values(startDate, endDate):
    try:
        data = {}
        ts=time.time()
        
        timestampold = datetime.datetime.strptime(startDate, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.strptime(endDate, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
        
        response = table.scan(
            FilterExpression=Key('Timestamp').between(timestampold, timestamp)
        )
        #returns first item in the list of all items returned from teh query; as discussed in class
        items = response['Items']
        if len(items) > 0:
            data["co2"] = int(items[0]["CO2"])
            data["temperature"] = int(items[0]["Temperature"])
            data["light"] = int(items[0]["Light"])
            data["humidity"] = int(items[0]["Humidity"])

            return jsonify(data)

        else:
            return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})

    except Exception as err:
        print("Unexpected error:", err)
        pass
            
    return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})
#data from the last minute
@APP.route('/recentData')
def recent_data():
    try:
        data = {}
        ts=time.time()
        ts = ts - (60*60*4) #converting utc to est
        timestampold = datetime.datetime.fromtimestamp(ts-60).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        response = table.scan(
            FilterExpression=Key('Timestamp').between(timestampold, timestamp)
        )
        co2 = []
        temp = []
        light = []
        humidity = []
        mx = dict()
        mn = dict()
        mean = dict()
        data = dict()
        
        items = response['Items']
        for item in items:
            co2.append(int(item["co2"]))
            temp.append(int(item["Temperature"]))
            light.append(int(item["Light"]))
            humidity.append(int(item["Humidity"]))
        
        mx["co2"] = max(co2)
        mx["temperature"] = max(temp)
        mx["light"] = max(light)
        mx["humidity"] = max(humidity)
        
        mn["co2"] = min(co2)
        mn["temperature"] = min(temp)
        mn["light"] = min(light)
        mn["humidity"] = min(humidity)
        
        mean["co2"] = avg(co2)
        mean["temperature"] = avg(temp)
        mean["light"] = avg(light)
        mean["humidity"] = avg(humidity)
        
        data["max"] = mx
        data["min"] = mn
        data["mean"] = mean
        #return jsonify(data)
        return render_template('recentData.html', data = data)

    except Exception as err:
        print("Unexpected error:", err)
        pass
            
    return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})
@APP.route('/data')
def get_Data():
    try:
        data = {}
        ts=time.time()
        ts = ts - (60*60*4) #converting utc to est
        timestampold = datetime.datetime.fromtimestamp(ts-60).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        response = table.scan(
            FilterExpression=Key('Timestamp').between(timestampold, timestamp)
        )
        
        items = response['Items']
        if len(items) > 0:
            data["co2"] = int(items[0]["CO2"])
            data["temperature"] = int(items[0]["Temperature"])
            data["light"] = int(items[0]["Light"])
            data["humidity"] = int(items[0]["Humidity"])

            return jsonify(data)

        else:
            return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})

    except Exception as err:
        print("Unexpected error:", err)
        pass
            
    return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})

@APP.route('/')
def index():
    return render_template('dashboard.html')


if __name__ == '__main__':
    APP.debug=True
    APP.run(host='0.0.0.0', port=80)