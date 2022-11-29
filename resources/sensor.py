from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from models.sensor import SensorModel
from datetime import datetime
from secrets import token_urlsafe



class Sensor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "api_key", type=str, required = False, help="MISSING: Unique name of your sensor."
    )
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
        "aqius", type=int, required = False, help="MISSING: AQI value based on US EPA standard."
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
        if name == None:
            return {"message":"Your sensor have no name"}, 404
        item = SensorModel.find_by_id(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required()
    def post(self, name):
        if SensorModel.find_by_name(name) :
            return{
                "message": "A sensor with name '{}' already exists.".format(name)
            }, 400
        
        data = Sensor.parser.parse_args()

        item = SensorModel(name, **data)
        item.timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        while True:
            item.api_key = token_urlsafe(16)
            if not (SensorModel.find_by_api_key(item.api_key)):
                break

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500

        return {"api_key": item.api_key}, 201

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

    #@jwt_required()
    def put(self, name):
        data = Sensor.parser.parse_args()

        item = SensorModel.find_by_name(name)

        if item:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if now - item.timestamp > 60:
                if(data["api_key"]==item.api_key):
                    item.city = data["city"]
                    item.location_x = data["location_x"]
                    item.location_y = data["location_y"]
                    item.timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    item.aqius = data["aqius"]
                    item.main = data["main"]
                    item.temperature = data["temperature"]
                    item.pressure = data["pressure"]
                    item.humidity = data["humidity"]
                    item.wind_spd = data["wind_spd"]
                    item.wind_dir = data["wind_dir"]
                else:
                    return {"message": "Api key is not valid."}, 404
            else:
                return {"message": "You are sending data too fast."}, 404  
        else:
            return {"message": "No item found."}, 404
        item.save_to_db()
        return item.json() 


class SensorList(Resource):
    @jwt_required()
    def get(self):
       # items = [item.json() for item in SensorModel.find_all()]
        items = []
        for item in SensorModel.find_all(): 
            template={
                "id": item.id,
                "name": item.name,
                "city": item.city,
                'location_x': item.location_x,
                'location_y': item.location_y,
                "aqius": item.aqius,
                "main": item.main
                }
            items.append(template)
        return{
            "sensors": items
        }, 200