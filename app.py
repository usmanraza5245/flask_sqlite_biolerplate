#!flask/bin/python
from flask import Flask, jsonify, render_template, redirect, request, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask import request
import json
import snscrape.modules.twitter as sntwitter
from datetime import datetime
import json
from models.user import User
from models.target import Target
from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
# Github Token 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
# Github user ratroot92

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '004f2af45d3a4e161a7dd2d17fdae47f'

# innitliaze DB

# userTargetCollection = db['usertargets']
# usersCollection = db['users']


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            authUser = db.users.find_one({'email': data["email"]})
            data = {"_id": str(authUser["_id"]), "username": authUser["username"],
                    "firstName": authUser["firstName"], "lastName": authUser["lastName"], "email": authUser["email"]}
        except Exception as e:
            return jsonify({'message': e})

        return f(data, *args, **kwargs)
    return decorator


# create a function
def __repr__(self):
    return '<Name %r>' % self.id


@app.route('/user', methods=['POST'])
def createUser():
    try:
        reqBody = request.get_json()
        if reqBody is None:
            return jsonify({"success": 'false', 'message': 'Invalid JSON'}), 400
        user = User(
            firstName=reqBody["firstName"],
            lastName=reqBody["lastName"],
            username=reqBody["username"],
            password=reqBody["password"],
            email=reqBody["email"]
        )
        exists = User.UserExists(
            {'username': reqBody['username'], 'email': reqBody['email']})
        if not exists:
            user = db.users.insert_one(user.toDictionary())
            user = db.users.find_one({'_id': user.inserted_id})
            data = {"_id": str(user["_id"]), "username": user["username"],
                    "firstName": user["firstName"], "lastName": user["lastName"], "email": user["email"]}
            response = make_response(jsonify(
                {"data": data, "message": "User created successfully", "success": True}), 200)
            return response
        else:
            response = make_response(
                jsonify({"message": "User already exists", "success": False}), 200)
            return response
    except Exception as e:
        errResponse = make_response(
            jsonify({"message": e, "success": False}), 500)
        return response


@app.route('/user', methods=['GET'])
@token_required
def getAllUsers(authUser):
    try:
        data = []
        users = db.users.find()
        for user in users:
            data.append({"_id": str(user["_id"]), "username": user["username"],
                        "firstName": user["firstName"], "lastName": user["lastName"], "email": user["email"]})
        response = make_response(
            jsonify({"data": data, "message": "All users", "success": True}), 200)
        return response
    except Exception as e:
        errResponse = make_response(
            jsonify({"message": e, "success": False}), 500)
        return response


@app.route('/login', methods=['POST'])
def login():
    try:
        reqBody = request.get_json()
        if 'email' not in reqBody:
            return jsonify({"success": 'false', 'message': 'email is required.'}), 400
        if 'password' not in reqBody:
            return jsonify({"success": 'false', 'message': 'password is required.'}), 400

        user = User.UserExists(
            {'email': reqBody['email'], 'password': reqBody['password']})
        if not user:

            response = make_response(
                jsonify({"data": {}, "message": "Invalid credentials", "success": False}), 401)
            return response
        else:
            data = {"_id": str(user["_id"]), "email": user["username"], "firstName": user["firstName"],
                    "lastName": user["lastName"], "email": user["email"]}
            token = jwt.encode({'email': data["email"], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
            response = make_response(jsonify(
                {"data": data, "message": "Logged in successfully", "success": True, "token": token}), 200)
            return response
    except Exception as e:
        errResponse = make_response(
            jsonify({"message": e, "success": False}), 500)
        return response


@app.route('/user/seed', methods=['GET'])
def seed():
    try:
        data = User.seed()
        response = make_response(jsonify(
            {"data": data, "message": "User seed successfully", "success": True}), 200)
        return response
    except Exception as e:
        errResponse = make_response(
            jsonify({"message": e, "success": False}), 500)
        return response


@app.route('/user/targets/keywords', methods=['POST'])
@token_required
def setUserTargets(authUser):
    try:
        reqBody = request.get_json()
        if 'targetType' not in reqBody:
            return jsonify({"success": 'false', 'message': 'targetType is required.'}), 400
        if reqBody['targetType'] != 'keywords' or reqBody['targetType'] != 'hashtags' or reqBody['targetType'] != 'username':
            return jsonify({"success": 'false', 'message': 'Invalid "targeType" .'}), 400
        if 'targets' not in reqBody and len(reqBody.targets) == 0:
            return jsonify({"success": 'false', 'message': 'targets is required.'}), 400
        exist = Target.TargetExist(reqBody)
        if not exist:
            target = Target(
                targetType=reqBody["targetType"],
                targets=reqBody["targets"],
                user=authUser['_id']
            )
            target = db.targets.insert_one(target.toDictionary())
            target = db.targets.find_one({'_id': target.inserted_id})
            data = {"_id": str(target["_id"]), "targetType": target["targetType"],
                    "targets": target["targets"], "user": target["user"]}
            response = make_response(jsonify(
                {"data": data, "message": "Target created successfully", "success": True}), 200)
            return response
        else:
            response = make_response(jsonify(
                {"data": [], "message": "Target Type '" + reqBody["targetType"]+"' already exists.", "success": True, }), 200)
            return response

    except Exception as e:
        errResponse = make_response(jsonify({"message": e}), 200)
        return response


@app.route('/user/targets/keywords', methods=['GET'])
@token_required
def getUserTargets(authUser):
    try:
        targets = db.targets.find({'user': authUser['_id']})
        data = []
        for target in targets:
            data.append({"_id": str(target["_id"]), "targetType": target["targetType"],
                        "targets": target["targets"], "user": target["user"]})
        response = make_response(jsonify(
            {"data": data, "message": "Target created successfully", "success": True}), 200)
        return response
    except Exception as e:
        errResponse = make_response(jsonify({"message": e}), 200)
        return response


@app.route('/target', methods=['GET', 'POST'])
def any():
    try:
        reqBody = request.get_json()

    except Exception as e:
        errResponse = make_response(jsonify({"message": e}), 200)
        return response


@app.route('/submitForm', methods=['POST', 'GET'])
def submitForm():
    if request.method == "POST":
        # fetch values from post form
        inputFromForm = request.form['text']
        # save to db
        try:
            newSuggestionObject = Suggestions(suggestion1="suggesttion1", suggestion2="suggesttion2",
                                              suggestion3="suggesttion3", suggestion4="suggesttion4", suggestion5="suggesttion5")
            db.session.add(newSuggestionObject)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return redirect("/")
    else:
        return redirect("/")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(app.run(port=5000, debug=True))
    loop.run_forever()
    # flask --app app.py --debug run
