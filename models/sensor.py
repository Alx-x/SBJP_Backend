from time import time
from db import db

class SensorModel(db.Model):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    api_key = db.Column(db.String(80), unique=True)

    city = db.Column(db.String(80))
    location_x = db.Column(db.Float(precision=10))
    location_y = db.Column(db.Float(precision=10))
    timestamp = db.Column(db.String(80)) #timestamp

    aqius = db.Column(db.Integer) #AQI value based on US EPA standard
    main = db.Column(db.String(80)) #main pollutant for AQI
                                    #"units":  //object containing units information
                                    #"p2": "ugm3", //pm2.5
                                    #"p1": "ugm3", //pm10
                                    #"o3": "ppb", //Ozone O3
                                    #"n2": "ppb", //Nitrogen dioxide NO2 
                                    #"s2": "ppb", //Sulfur dioxide SO2 
                                    #"co": "ppm" //Carbon monoxide CO 
                                    #                        
    temperature = db.Column(db.Integer) #celcius
    pressure = db.Column(db.Integer) #hPa
    humidity = db.Column(db.Integer) # %
    wind_spd = db.Column(db.Float(precision=2)) #speed m/s
    wind_dir = db.Column(db.Integer) #wind direction, as an angle of 360° (N=0, E=90, S=180, W=270)
    
    def __init__(self, name, api_key, city, location_x, location_y, timestamp, aqius, main, temperature, pressure, humidity, wind_spd, wind_dir):
        self.name = name
        self.api_key = None
        self.city = city
        self.location_x = location_x
        self.location_y = location_y
        self.timestamp = timestamp
        self.aqius = aqius
        self.main = main
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.wind_spd = wind_spd
        self.wind_dir = wind_dir

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'location_x': self.location_x,
            'location_y': self.location_y,
            'timestamp': self.timestamp,
            'aqius': self.aqius,
            'main': self.main,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'wind_spd': self.wind_spd,
            'wind_dir': self.wind_dir
        }
    
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_api_key(cls, api_key):
        return cls.query.filter_by(api_key=api_key).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
