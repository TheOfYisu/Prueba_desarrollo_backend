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


@app.route('/getvehicle', methods=['GET'])
def getvehicle():
    try:
        vehicles = Vehicles.select()
        listvehicle = []
        for Vehicle in vehicles:
            content = {'ID': Vehicle.id, 'DESCRIPTION': Vehicle.description, 'YEAR': Vehicle.year, 'MAKE': Vehicle.make,
                       'CAPACITY': Vehicle.capacity, 'ACTIVE': Vehicle.active}
            listvehicle.append(content)
        return jsonify(listvehicle)
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/addvehicle', methods=['POST'])
def addvehicle():
    try:
        print(request.json)
        DESCRIPTION = request.json['DESCRIPTION']
        YEAR = int(request.json['YEAR'])
        MAKE = int(request.json['MAKE'])
        CAPACITY = int(request.json['CAPACITY'])
        ACTIVE = int(request.json['ACTIVE'])
        vehicle = Vehicles(description=DESCRIPTION, year=YEAR, make=MAKE, capacity=CAPACITY, active=ACTIVE)
        vehicle.save()
        return jsonify("listdrivers")
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/getroutes', methods=['GET'])
def getroutes():
    try:
        routes = Routes.select()
        listroute = []
        for route in routes:
            driver = Drivers.get(Drivers.id == route.drivers_id)
            vehicle = Vehicles.get(Vehicles.id == route.vehicle_id)
            namedriver = "{} {}".format(driver.first_name, driver.last_name)
            vehiclemake = vehicle.make
            content = {"ID": route.id, "DESCRIPTION": route.description, "DRIVER": namedriver, "VEHICLE": vehiclemake,
                       "ACTIVE": route.active}
            listroute.append(content)
        return jsonify(listroute)
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/getifoformsrouter', methods=['GET'])
def getifoformsrouter():
    try:
        drivers = Drivers.select()
        vehicles = Vehicles.select()
        listdrivers = []
        listvehicle = []
        for driver in drivers:
            namedriver = "{} {}".format(driver.first_name, driver.last_name)
            content = {"ID": driver.id, "NAMEDRIVER": namedriver}
            listdrivers.append(content)
        for vehicle in vehicles:
            content = {"ID": vehicle.id, "MAKE": vehicle.make}
            listvehicle.append(content)
        return jsonify({"listdriver": listdrivers, "listvehicle": listvehicle})
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/addroute', methods=['POST'])
def addroute():
    try:
        DESCRIPTION = request.json['DESCRIPTION']
        DRIVER = int(request.json['DRIVER'])
        VEHICLE = int(request.json['VEHICLE'])
        ACTIVE = int(request.json['ACTIVE'])
        route = Routes(description=DESCRIPTION, drivers_id=DRIVER, vehicle_id=VEHICLE, active=ACTIVE)
        route.save()
        return jsonify("listdrivers")
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/getroute/<idroute>', methods=['GET'])
def getroute(idroute):
    try:
        route = Routes.get(Routes.id == idroute)
        driver = Drivers.get(Drivers.id == route.drivers_id)
        vehicle = Vehicles.get(Vehicles.id == route.vehicle_id)
        content = {"ID_ROUTE": route.id, "DESCRIPTION_ROUTE": route.description, "ACTIVE_ROUTE": route.active}
        content2 = {'ID_VEHICLE': vehicle.id, 'DESCRIPTION_VEHICLE': vehicle.description, 'CAPACITY': vehicle.capacity}
        content3 = ({'ID_DRIVER': driver.id, 'LAST_NAME': driver.last_name, 'FIRST_NAME': driver.first_name,
                     'ADDRESS': driver.address, 'CITY': driver.city, 'PHONE': driver.phone})
        return jsonify({"DATAROUTER": content, "DATAVEHICLE": content2, "DATADRIVER": content3})
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/deleteroute/<idroute>', methods=['DELETE'])
def deleteroute(idroute):
    try:
        routedelete = Routes.get(Routes.id == idroute)
        routedelete.delete_instance()
        return jsonify("Dato eliminado")
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/updateroute/<idroute>', methods=['PUT'])
def updateroute(idroute):
    try:
        DESCRIPTION = request.json['DESCRIPTION']
        DRIVER = int(request.json['DRIVER'])
        VEHICLE = int(request.json['VEHICLE'])
        ACTIVE = int(request.json['ACTIVE'])
        Routes.update(description=DESCRIPTION, drivers_id=DRIVER, vehicle_id=VEHICLE, active=ACTIVE).where(
            Routes.id == idroute).execute()
        return jsonify("listdrivers")
    except Exception as e:
        return jsonify({"informacion": e})

@app.route('/deletevehicle/<idvehicle>', methods=['DELETE'])
def deletevehicle(idvehicle):
    try:
        driverdeleter = Vehicles.get(Vehicles.id == idvehicle)
        driverdeleter.delete_instance()
        return jsonify("Dato eliminado")
    except Exception as e:
        return jsonify({"informacion": e})


@app.route('/updatevehicle/<idvehicle>', methods=['PUT'])
def updatevehicle(idvehicle):
    try:
        DESCRIPTION = request.json['DESCRIPTION']
        YEAR = int(request.json['YEAR'])
        MAKE = int(request.json['MAKE'])
        CAPACITY = int(request.json['CAPACITY'])
        ACTIVE = int(request.json['ACTIVE'])
        Vehicles.update(description=DESCRIPTION, year=YEAR, make=MAKE, capacity=CAPACITY, active=ACTIVE).where(
            Vehicles.id == idvehicle).execute()
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
