from flask import Flask
from flask import request
import pymongo 
import datetime


app = Flask(__name__)

password = "fEFEs0Y0WSuyl6YC"
uri = f"mongodb+srv://dismtzking:{password}@cluster0.9vjmeo5.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(uri)

db = client['db_iot_1']
my_collections = db['collection_iot_1']

def kirim_data(kecepatan,longitude,latitude,timestamp):
    sensor = {
        'kecepatan':kecepatan,
        'longitude':longitude,
        'latitude':latitude,
        'timestamp':timestamp
    }
    results = my_collections.insert_one(sensor)

@app.route('/', methods =['GET'])
def hello_world():
    return 'HELLO DUNIA'

@app.route('/gps', methods =['POST'])
def gps():

    kecepatan = request.args.get('kecepatan')
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    timestamp = datetime.datetime.now()

    if kecepatan is not None:
        kecepatan = float(kecepatan)
    if longitude is not None:
        longitude = float(longitude)
    if latitude is not None:
        latitude = float(latitude)

    kirim_data(kecepatan=kecepatan,longitude=longitude, latitude =latitude, timestamp =timestamp)

    return f'kecepatan:{kecepatan}km, longitude:{longitude}, latitude:{latitude}, timestamp:{timestamp}'

if __name__ == '__main__':
    app.run(host='0.0.0.0')