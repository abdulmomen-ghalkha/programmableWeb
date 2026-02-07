from flask_restful import Resource, Api
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)


class SensorCollection(Resource):
    def get(self):
        pass
    def post(self):
        pass

class SensorItem(Resource):
    def get(self, sensor):
        pass
    
    def put(self, sensor):
        pass
    
    def delete(slef, sensor):
        pass


api.add_resource(SensorCollection, "/api/sensors/")
api.add_resource(SensorItem, "/api/sensros/<sensor>/")

