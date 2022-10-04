from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from models.sensor import SensorModel
from datetime import datetime



class Sensor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "city", type=str, required = False, help="MISSING: The city where the sensor is located."
    )
    parser.add_argument(
        "location_x", type=float, required = True, help="MISSING: First of two coordinates."
    )
    parser.add_argument(
        "location_y", type=float, required = True, help="MISSING: Second of two coordinates."
    )
    parser.add_argument(
        "timestamp", type=str, required = False, help="MISSING: Time the data was sent."
    )
    parser.add_argument(
        "aqius", type=int, required = True, help="MISSING: AQI value based on US EPA standard."
    )
    parser.add_argument(
        "main", type=str, required = False, help="MISSING: Main pollutant for AQI."
    )
    parser.add_argument(
        "temperature", type=int, required = False, help="MISSING: Temperature in Celsius."
    )
    parser.add_argument(
        "pressure", type=int, required = False, help="MISSING: Atmospheric pressure in hPa."
    )
    parser.add_argument(
        "humidity", type=int, required = False, help="MISSING: Humidity in %."
    )
    parser.add_argument(
        "wind_spd", type=float, required = False, help="MISSING: Wind speed in (m/s)."
    )
    parser.add_argument(
        "wind_dir", type=int, required = False, help="MISSING:Wind direction, as an angle of 360° (N=0, E=90, S=180, W=270)."
    )


    @jwt_required()
    def get(self, name):
        item = SensorModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name = None):
        APIDATA =['Wroclaw-API', 'Poznan-API', 'Bydgoszcz-API',
                    'Torun-API', 'Krakow-API', 'Lodz-API',
                    'Warsaw-API', 'Bialystok-API', 'Gdansk-API',
                    'Katowice-API', 'Rzeszow-API', 'Kielce-API',
                    'Olsztyn-API', 'Szczecin-API'
                    ]
        if SensorModel.find_by_name(name) or name in APIDATA :
            return{
                "message": "A sensor with name '{}' already exists.".format(name)
            }, 400
        
        data = Sensor.parser.parse_args()

        item = SensorModel(name, **data)
        item.timestamp = str(datetime.now())

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {"message": "Admin privilege required."}, 401

        item = SensorModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}
        return {"message": "Item not found."}, 404

    @jwt_required()
    def put(self, name):
        data = Sensor.parser.parse_args()

        item = SensorModel.find_by_name(name)

        if item:
            item.city = data["city"]
            item.location_x = data["location_x"]
            item.location_y = data["location_y"]
            item.timestamp = str(datetime.now())
            item.aqius = data["aqius"]
            item.main = data["main"]
            item.temperature = data["temperature"]
            item.pressure = data["pressure"]
            item.humidity = data["humidity"]
            item.wind_spd = data["wind_spd"]
            item.wind_dir = data["wind_dir"]
        else:
            item = SensorModel(name, **data)
            item.timestamp = str(datetime.now())

        item.save_to_db()

        return item.json()

class SensorList(Resource):
    @jwt_required()
    def get(self):
        items = [item.json() for item in SensorModel.find_all()]
        return{
            "sensors": items
        }, 200