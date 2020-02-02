#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource, reqparse
from configparser import ConfigParser
import psycopg2

app = Flask(__name__)
api = Api(app)

regions = {
  1 : "Adygeya Republic",
  2 : "Bashkortostan Republic",
  3 : "Buryatiya Republic",
  4 : "Altaj Republic",
  5 : "Dagestan Republic",
  8 : "Kalmykiya Republic"
}

def db_config(filename='database.ini', section='postgresql'):
  parser = ConfigParser()
  parser.read(filename)
  db = {}
  if parser.has_section(section):
    params = parser.items(section)
    for param in params:
      db[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in the {1} file'.format(section, filename))
  return db

def db_init():
  conn = None
  try:
    db_params = db_config()
    print("Initial connecting to the PostgreSQL database...")
    conn = psycopg2.connect(**db_params)
    print("Take cursor")
    cur = conn.cursor()
    init_transaction = ("""
      CREATE TABLE regions (
        region_id INTEGER PRIMARY KEY,
        region_name VARCHAR(255) NOT NULL
      );
      CREATE TABLE citizens (
        region_id INTEGER NOT NULL,
        citizen_id SERIAL PRIMARY KEY,
        citizen_name VARCHAR(255) NOT NULL,
        citizen_lastname VARCHAR(255) NOT NULL,
        citizen_age INTEGER NOT NULL,
        citizen_email VARCHAR(255) NOT NULL,
        FOREIGN KEY (region_id)
          REFERENCES regions (region_id)
          ON UPDATE CASCADE ON DELETE CASCADE
      );
      """)
    print("Execute initial transaction")
    cur.execute(init_transaction)
    for reg_id in regions.keys():
      print("Insert region " + str(reg_id) + " : " + regions[reg_id])
      reg_name = regions[reg_id]
      cur.execute("INSERT INTO regions(region_id, region_name) VALUES(%s, %s);", (reg_id, reg_name))
    cur.close()
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
      conn.close()
      print("Database connection closed")

class Quote(Resource):
  # Returns citizens in region
  # example: curl http://127.0.0.1:5000/region/8
  def get(self, region_id = 1):
    global regions
    try:
      if region_id in regions.keys():
        db_params = db_config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)
        print("Take cursor")
        cur = conn.cursor()
        print("Execute GET transaction")
        cur.execute("""SELECT region_name, citizen_name, citizen_lastname, citizen_age, citizen_email
          FROM regions INNER JOIN citizens ON regions.region_id = citizens.region_id
          WHERE regions.region_id = %s;""", (region_id, ))
        result = cur.fetchall()
        cur.close()
        return result, 200
      return f"Region with id {region_id} not found", 404
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()
        print("Database connection closed")

  # Add new citizen to region
  # example: curl -X POST http://127.0.0.1:5000/region/8?"name"="Fedor"&"lastname"="Sumkin"&"age"=37&"email"="test@mail.com"
  def post(self, region_id = 1):
    global regions
    try:
      if region_id in regions.keys():
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("lastname")
        parser.add_argument("age")
        parser.add_argument("email")
        req_params = parser.parse_args()
        db_params = db_config()
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**db_params)
        print("Take cursor")
        cur = conn.cursor()
        print("Execute POST transaction")
        cur.execute("""INSERT INTO citizens(region_id, citizen_name, citizen_lastname, citizen_age, citizen_email)
          VALUES(%s, %s, %s, %s, %s);
          """, (region_id, req_params["name"], req_params["lastname"], req_params["age"], req_params["email"]))
        conn.commit()
        cur.close()
        return f"Region citizen was added", 200
      return f"Region with id {region_id} not found", 404
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      if conn is not None:
        conn.close()
        print("Database connection closed")

api.add_resource(Quote, "/region", "/region/", "/region/<int:region_id>")
if __name__ == '__main__':
  db_init()
  app.run(debug=True)
