from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config.from_object("app.config.Config")
api = Api(app)
db = SQLAlchemy(app)

class Region(db.Model):
  __tablename__ = "regions"

  region_code = db.Column(db.Integer, unique=True, primary_key=True)
  region_name = db.Column(db.String(128), unique=True, nullable=False)
  citizens = db.relationship("Citizen")

  def __init__(self, region_code, region_name):
      self.region_code = region_code
      self.region_name = region_name

class Citizen(db.Model):
  __tablename__ = "citizens"

  citizen_id = db.Column(db.Integer, unique=True, primary_key=True)
  citizen_name = db.Column(db.String(128), nullable=False)
  citizen_lastname = db.Column(db.String(128), nullable=False)
  citizen_age = db.Column(db.Integer, nullable=False)
  citizen_email = db.Column(db.String(128), nullable=False)

  region_code = db.Column(db.Integer, db.ForeignKey('regions.region_code'))

  def __init__(self, region_code, citizen_name, citizen_lastname, citizen_age, citizen_email):
    self.region_code = region_code
    self.citizen_name = citizen_name
    self.citizen_lastname = citizen_lastname
    self.citizen_age = citizen_age
    self.citizen_email = citizen_email

class Quote(Resource):
  # Returns citizens in region
  # example: curl http://127.0.0.1:5000/region/8
  def get(self, region_code = 1):
    try:
      print("Execute GET transaction")
      result = db.session.query(Region.region_name, Citizen.citizen_name, Citizen.citizen_lastname, Citizen.citizen_age, Citizen.citizen_email).filter(Region.region_code == Citizen.region_code).filter(Region.region_code == region_code).all()
      return result, 200
    except (Exception, flask_sqlalchemy.sqlalchemy.exc.SQLAlchemyError) as error:
      print(error)
    finally:
      db.session.close()

  # Add new citizen to region
  # example: curl -X POST http://127.0.0.1:5000/region/8?"name"="Fedor"&"lastname"="Sumkin"&"age"=37&"email"="test@mail.com"
  def post(self, region_code = 1):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument("name")
      parser.add_argument("lastname")
      parser.add_argument("age")
      parser.add_argument("email")
      req_params = parser.parse_args()
      db.session.add(Citizen(region_code=region_code, citizen_name=req_params["name"], citizen_lastname=req_params["lastname"], citizen_age=req_params["age"], citizen_email=req_params["email"]))
      db.session.commit()
      return f"Region' citizen was added", 200
    except (Exception, flask_sqlalchemy.sqlalchemy.exc.SQLAlchemyError) as error:
      print(error)
    finally:
      db.session.close()

api.add_resource(Quote, "/region", "/region/", "/region/<int:region_code>")
