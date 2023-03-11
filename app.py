#!flask/bin/python
from flask import Flask, jsonify ,render_template, redirect,request,make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask import request
import json
import snscrape.modules.twitter as sntwitter
from datetime import datetime
import json
from models.user import User
from config.db import db 

from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import uuid
import jwt
import datetime


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'

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
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = db.users.find_one({'_id':data["_id"]})
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator






#create a function 
def __repr__(self):
    return '<Name %r>' % self.id



@app.route('/user', methods=['POST'])
def createUser():
   try:
        reqBody = request.get_json()
        if reqBody is None:
            return jsonify({'error': 'Invalid JSON'}), 400
        user = User(
           firstName=reqBody["firstName"],
           lastName=reqBody["lastName"],
           username=reqBody["username"],
           password=reqBody["password"],
           email=reqBody["email"]
        )
        exists=User.UserExists({'username':reqBody['username'],'email':reqBody['email']})
        if not exists:
            user=db.users.insert_one(user.toDictionary())
            user=db.users.find_one({'_id':user.inserted_id})
            data ={"_id": str(user["_id"]),"username":user["username"],"firstName":user["firstName"],"lastName":user["lastName"],"email":user["email"]}
            response = make_response(jsonify({"data":data,"message":"User created successfully","success":True}), 200)
            return response
        else:
            response = make_response(jsonify({"message":"User already exists","success":False}), 200)
            return response
   except Exception as e:
        errResponse = make_response(jsonify({"message":e,"success":False}), 500)
        return response




@app.route('/user', methods=['GET'])
@token_required
def getAllUsers(current_user):
    try:
        data=[]
        users=db.users.find()
        for user in users:
            data.append({"_id": str(user["_id"]),"username":user["username"],"firstName":user["firstName"],"lastName":user["lastName"],"email":user["email"]})
        response = make_response(jsonify({"data":data,"message":"All users","success":True}), 200)
        return response
    except Exception as e:
        errResponse = make_response(jsonify({"message":e,"success":False}), 500)
        return response

@app.route('/login', methods=['POST'])
def login():
    try:
        reqBody = request.get_json()
        if 'email' not in reqBody:
            return jsonify({'error': 'email is required.'}), 400
        if 'password' not in reqBody:
            return jsonify({'error': 'password is required.'}), 400

        user=User.UserExists({'email':reqBody['email'],'password':reqBody['password']})
        if not user:

            response= make_response(jsonify({"data":{},"message":"Invalid credentials","success":False}), 401)
            return response
        else:
            data ={"_id": str(user["_id"]),"email":user["username"],"firstName":user["firstName"],"lastName":user["lastName"],"email":user["email"]}
            token = jwt.encode({'_id' : data["_id"], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256")
            response = make_response(jsonify({"data":data,"message":"Logged in successfully","success":True,"token":token}), 200)
            return response
    except Exception as e:
        errResponse = make_response(jsonify({"message":e,"success":False}), 500)
        return response

@app.route('/seed', methods=['GET'])
def seed():
    try:
        data=User.seed()
        response = make_response(jsonify({"data":data,"message":"User seed successfully","success":True}), 200)
        return response
    except Exception as e:
        errResponse = make_response(jsonify({"message":e,"success":False}), 500)
        return response

@app.route('/target/profile', methods=['GET','POST'])
def getTwitterProfile():
   try:
        reqBody = request.get_json()
        if(reqBody["targetUsername"]):
            arr=[]
            scrapper=sntwitter.TwitterProfileScraper(reqBody["targetUsername"])
            for index,tweet in enumerate(scrapper.get_items()):
                # arr.append([tweet.date,tweet.id,tweet.rawContent,tweet.user.username,tweet.likeCount,tweet.retweetCount])
                arr.append(tweet)
                if index>2:
                    break
            response = make_response(jsonify(arr), 200)
            return response
        else:
            raise Exception("targetUsername is required!")
   except Exception as e:
        errResponse = make_response(jsonify({"message":e}), 200)
        return response



@app.route('/target', methods=['GET','POST'])
def any():
   try:
        reqBody = request.get_json()
        
   except Exception as e:
        errResponse = make_response(jsonify({"message":e}), 200)
        return response





@app.route('/submitForm',methods=['POST','GET'])
def submitForm():
    if request.method== "POST":
        #fetch values from post form 
        inputFromForm=request.form['text']
        #save to db 
        try:
            newSuggestionObject=Suggestions(suggestion1="suggesttion1",suggestion2="suggesttion2",suggestion3="suggesttion3",suggestion4="suggesttion4",suggestion5="suggesttion5")
            db.session.add(newSuggestionObject)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return redirect("/")
    else:
        return redirect("/")





if __name__ == '__main__':
    app.run()
    # flask --app app.py --debug run