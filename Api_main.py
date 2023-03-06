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
    drivers_id = ForeignKeyField(Drivers, backref='routes')
    vehicle_id = ForeignKeyField(Vehicles, backref='routes')
    active = BooleanField()

    class Meta:
        database = db


class Schedules(Model):
    id = AutoField(primary_key=True)
    route_id = ForeignKeyField(Routes, backref='schedules')
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
        query = Users.select(Users.password).where(Users.user == user)
        if query:
            passworduser = query.get()
            if password == passworduser.password:
                username = passworduser.username
                jwt_token = jwt_api.generar_jwt({"usuario": user})
                return jsonify({"token": jwt_token, "State": "True", "Username": username})
            else:
                return jsonify({"State": "False"})
        else:
            return jsonify({"State": "False"})
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/getdrivers', methods=['GET'])
def getdrivers():
    try:
        drivers = Drivers.select()
        listdrivers = []
        for driver in drivers:
            content = (
                {'ID': driver.id, 'LAST_NAME': driver.last_name, 'FIRST_NAME': driver.first_name, 'SSD': driver.ssd,
                 'DOB': driver.dob, 'ADDRESS': driver.address, 'CITY': driver.city, 'ZIP': driver.zip,
                 'PHONE': driver.phone, 'ACTIVE': driver.active})
            listdrivers.append(content)
        return jsonify(listdrivers)
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/adddrivers', methods=['POST'])
def adddrivers():
    try:
        LAST_NAME = request.json['LAST_NAME']
        FIRST_NAME = request.json['FIRST_NAME']
        SSD = request.json['SSD']
        DOB = request.json['DOB']
        ADDRESS = request.json['ADDRESS']
        CITY = request.json['CITY']
        ZIP = request.json['ZIP']
        PHONE = int(request.json['PHONE'])
        ACTIVE = int(request.json['ACTIVE'])
        driver = Drivers(last_name=LAST_NAME, first_name=FIRST_NAME, ssd=SSD, dob=DOB, address=ADDRESS, city=CITY,
                         zip=ZIP, phone=PHONE, active=ACTIVE)
        driver.save()
        return jsonify("listdrivers")
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/deletedriver/<iddriver>', methods=['DELETE'])
def deletedrivers(iddriver):
    try:
        driverdeleter = Drivers.get(Drivers.id == iddriver)
        driverdeleter.delete_instance()
        return jsonify("Dato eliminado")
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/updatedriver/<iddriver>', methods=['PUT'])
def updatedriver(iddriver):
    try:
        LAST_NAME = request.json['LAST_NAME']
        FIRST_NAME = request.json['FIRST_NAME']
        SSD = request.json['SSD']
        DOB = request.json['DOB']
        ADDRESS = request.json['ADDRESS']
        CITY = request.json['CITY']
        ZIP = request.json['ZIP']
        PHONE = int(request.json['PHONE'])
        ACTIVE = int(request.json['ACTIVE'])
        Drivers.update(last_name=LAST_NAME, first_name=FIRST_NAME, ssd=SSD, dob=DOB, address=ADDRESS, city=CITY,
                       zip=ZIP, phone=PHONE, active=ACTIVE).where(Drivers.id == iddriver).execute()
        return jsonify("Dato eliminado")
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
