import jwt_api
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
from peewee import *

app = Flask(__name__)
CORS(app)
app.secret_key = "mysecretkey"
db = MySQLDatabase('prueba_desarrollo_bd2', user='root', password='', host='localhost')

class Drivers(Model):
    id = AutoField(primary_key=True)
    last_name = CharField()
    first_name = CharField()
    ssd = CharField()
    dob = DateField()
    address = CharField()
    city = CharField()
    zip = IntegerField()
    phone = IntegerField()
    active = BooleanField()

    class Meta:
        database = db

class Vehicles(Model):
    id = AutoField(primary_key=True)
    description = CharField()
    year = IntegerField()
    make = IntegerField()
    capacity = IntegerField()
    active = BooleanField()

    class Meta:
        database = db

class Routes(Model):
    id = AutoField(primary_key=True)
    description = CharField()
    drivers_id  = ForeignKeyField(Drivers,backref='routes')
    vehicle_id  = ForeignKeyField(Vehicles,backref='routes')
    active = BooleanField()

    class Meta:
        database = db


class Schedules(Model):
    id = AutoField(primary_key=True)
    route_id  = ForeignKeyField(Routes,backref='schedules')
    week_num = IntegerField()
    fromm = DateTimeField()
    to = DateTimeField()
    active = BooleanField()

    class Meta:
        database = db

class Users(Model):
    id = AutoField(primary_key=True)
    user = CharField()
    password = CharField()
    username = CharField()

    class Meta:
        database = db

@app.route('/login', methods=['POST'])
def login():
    try:
        user = request.json['user']
        password = request.json['password']
        query=Users.select(Users.password).where(Users.user==user)
        if query:
            passworduser=query.get()
            if password==passworduser.password:
                username=passworduser.username
                jwt_token = jwt_api.generar_jwt({"usuario": user})
                return jsonify({"token": jwt_token,"State":"True","Username":username})
            else:
                return jsonify({"State":"False"})
        else:
            return jsonify({"State":"False"})
    except Exception as e:
        return jsonify({"informacion": e})

if __name__ == "__main__":
    if not Drivers.table_exists():
        db.create_tables([Drivers])
    if not Vehicles.table_exists():
        db.create_tables([Vehicles])
    if not Routes.table_exists():
        db.create_tables([Routes])
    if not Schedules.table_exists():
        db.create_tables([Schedules])
    if not Users.table_exists():
        db.create_tables([Users])
    app.run(port=5500, debug=True)