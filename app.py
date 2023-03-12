#!flask/bin/python
from flask import Flask, jsonify, render_template, redirect, request, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask import request
import asyncio
import json
import snscrape.modules.twitter as sntwitter
from datetime import datetime
import json
from models.user import User
from models.target import Target
from utils.snsscrapper import Scrapper
from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from multiprocessing import Process
from utils.util import Utils
import time
from apscheduler.schedulers.background import BackgroundScheduler


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
            print(">>>>>>>>>>>>>>", request.headers['x-access-tokens'])
            return Utils.UnauthorizedResponse('Missing access token.')
        try:
            tokenPayload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            authUser = db.users.find_one({'_id': ObjectId(tokenPayload['_id'])})
            authUser['_id'] = str(authUser['_id'])
            # data = {"_id": str(authUser["_id"]), "username": authUser["username"], "firstName": authUser["firstName"], "lastName": authUser["lastName"], "_id": authUser["_id"]}
        except Exception as e:
            return Utils.UnauthorizedResponse(e)
        return f(authUser, *args, **kwargs)
    return decorator


# create a function
def __repr__(self):
    return '<Name %r>' % self.id


@app.route('/user', methods=['POST'])
@token_required
def createUser(authUser):
    try:
        reqBody = request.get_json()
        if reqBody is None:
            return jsonify({"success": False, 'message': 'Invalid JSON'}), 400
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
            user['_id'] = str(user['_id'])
            # data = {"_id": str(user["_id"]), "username": user["username"], "firstName": user["firstName"], "lastName": user["lastName"], "email": user["email"]}
            return Utils.SuccessResponse(user, "User created successfully")
        else:
            return Utils.NotFoundResponse(user, "User already exists")
    except Exception as e:
        return Utils.ErrorResponse('Someting went wrong.')


@app.route('/user', methods=['GET'])
@token_required
def getAllUsers(authUser):
    try:
        data = []
        users = db.users.find()
        for user in users:
            data.append({"_id": str(user["_id"]), "username": user["username"],
                        "firstName": user["firstName"], "lastName": user["lastName"], "email": user["email"]})
        return Utils.SuccessResponse(data, "All users")
    except Exception as e:
        return Utils.ErrorResponse('Someting went wrong.')


@app.route('/login', methods=['POST'])
def login():
    try:
        reqBody = request.get_json()
        if 'email' not in reqBody:
            return Utils.BadRequestResponse('email is required.')
        if 'password' not in reqBody:
            return Utils.BadRequestResponse('password is required.')
        user = User.UserExists({'email': reqBody['email'], 'password': reqBody['password']})
        if not user:
            return Utils.UnauthorizedResponse('Invalid credentials.')
        else:
            data = {"_id": str(user["_id"]), "email": user["username"], "firstName": user["firstName"], "lastName": user["lastName"], "email": user["email"]}
            token = jwt.encode({'_id': data["_id"], 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
            response = make_response(jsonify({"data": data, "message": "Logged in successfully", "success": True, "token": token}), 200)
            return response
    except Exception as e:
        print(e)
        return Utils.ErrorResponse('Someting went wrong.')


@app.route('/user', methods=['DELETE'])
@token_required
def delete_user(authUser):
    try:
        db.targets.delete_many({'user': authUser['_id']})
        userId = ObjectId(authUser["_id"])
        result = db.users.delete_one({'_id': userId})
        if result.deleted_count == 1:
            return Utils.SuccessResponse(result, "User deleted successfully")
        else:
            return Utils.NotFoundResponse(userId, 'Error deleting user')

    except Exception as e:
        return Utils.ErrorResponse('Someting went wrong.')


@app.route('/user/seed', methods=['GET'])
def seed():
    try:
        data = User.seed()
        return Utils.SuccessResponse(data, "User seed successfully")
    except Exception as e:
        return Utils.ErrorResponse('Someting went wrong.')
# Define some heavy function


def scrapLater(exist):
    Scrapper.scrapKeywords(exist)
    print("Process Complete!!! for "+exist['_id']+" " + exist['targetType'])


@app.route('/user/targets/keywords', methods=['POST'])
@token_required
def setUserTargets(authUser):
    try:
        reqBody = request.get_json()
        if 'targetType' not in reqBody:
            return Utils.BadRequestResponse('targetType is required.')

        if reqBody['targetType'] != 'keywords' and reqBody['targetType'] != 'twitter-hashtag' and reqBody['targetType'] != 'twitter-user':
            return Utils.BadRequestResponse('Invalid "targetType" .')

        if 'targets' not in reqBody and len(reqBody['targets']) == 0:
            return Utils.BadRequestResponse('targets is required.')

        if 'limit' not in reqBody:
            return Utils.BadRequestResponse('limit is required.')

        if reqBody['limit'] > 1000:
            return Utils.BadRequestResponse('maximum limit is 1000.')

        exist = Target.TargetExist(reqBody)
        if not exist:
            target = Target(targetType=reqBody["targetType"], targets=reqBody["targets"], limit=reqBody['limit'], user=authUser['_id'])
            target = db.targets.insert_one(target.toDictionary())
            target = db.targets.find_one({'_id': target.inserted_id})
            target['_id'] = str(target['_id'])
            target['user'] = str(target['user'])
            # heavyTask = Process(target=scrapLater, args=(target,))
            # heavyTask.start()
            return Utils.SuccessResponse(target, "Target created successfully")
        else:
            response = Utils.NotFoundResponse(exist, "Target Type '" + reqBody["targetType"]+"' already exists.")
            return response

    except Exception as e:
        print(e)
        return Utils.ErrorResponse('Someting went wrong.')


@app.route('/user/targets/keywords', methods=['GET'])
@token_required
def getUserTargets(authUser):
    try:
        data = Target.GetUserTargets(authUser)
        return Utils.SuccessResponse(data, "All user targets.")
    except Exception as e:
        return Utils.ErrorResponse('Someting went wrong.')


@app.route('/user/targets/keywords', methods=['DELETE'])
@token_required
def deleteUserTargets(authUser):
    try:
        reqBody = request.get_json()
        if 'targetType' not in reqBody:
            return jsonify({"success": False, 'message': 'targetType is required.'}), 400
        else:
            db.targets.delete_many({'user': authUser['_id']})
            return Utils.SuccessResponse(authUser['_id'], "All users targets deleted successfully")
    except Exception as e:
        return Utils.ErrorResponse('Someting went wrong.')


def my_scheduler():
    targets = db.targets.find({})
    for target in targets:
        target['_id'] = str(target['_id'])
        scrapLater(target)


@app.before_first_request
def activate_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=my_scheduler, trigger='interval', seconds=10)
    scheduler.start()
    print(" >>> Scheduler started")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
