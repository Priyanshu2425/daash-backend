from flask import Flask, Blueprint, request, jsonify
from . import db
from .model import CurrentUser, Device, Data
from dataclasses import dataclass
import requests
from boltiot import Bolt
import json

api = Blueprint('api', __name__)

@api.route('/add-device', methods=['GET', 'POST'])
def add_device():
    print('did reach here')
    if request.method == "POST":
        device_name = request.json['deviceName']

        if len(device_name) < 1:
            print("device couldn't be added")
            return getDevices()
        
        currentUser = CurrentUser.query.get(1)

        new_device = Device(name=device_name, user_id=currentUser.current_user)
        db.session.add(new_device)
        db.session.commit()

        return getDevices()
    return "get request h ye toh"


@api.route('/get-devices', methods=["GET", "POST"])
def getDevices():
    curr_user_id = CurrentUser.query.get(1)
    devices = Device.query.filter_by(user_id=curr_user_id.current_user).all()
    device_list = []
    for d in devices:
        element = {}
        element[d.name] = d.id
        device_list.append(element)

    return jsonify([{'devices':device_list}])

@api.route('/add-data/<device_id_id>/<value_toadd>/')
def addDeviceDatum(device_id_id, value_toadd):
    curr_user_id = CurrentUser.query.get(1)
    
    if curr_user_id:
        print(value_toadd)
        if(int(value_toadd) > 0):
            new_datum = Data(datum=value_toadd,device_id=device_id_id)
            db.session.add(new_datum)
            db.session.commit()
            print('adding')
            return  jsonify([{'success':"data added"}])
    else: 
        print('No value')
        return jsonify([{'failure': "user not logged in"}])
        
    return jsonify([{'failure': "user not logged in"}])    

@api.route('/get-device-data/<device_id>')
def getDeviceData(device_id):
    current_user = CurrentUser.query.get(1)
    if(current_user):
        data_table = Data.query.filter_by(device_id=device_id).all()
        serialized_data = [device.to_dict() for device in data_table]
        return jsonify(serialized_data)
    return jsonify([{"failure":"none"}])

