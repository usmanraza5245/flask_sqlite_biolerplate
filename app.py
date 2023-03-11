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

from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import uuid
import jwt
import datetime


app = Flask(__name__)
app.debug = True


# innitliaze DB

# userTargetCollection = db['usertargets']
# usersCollection = db['users']











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
def getAllUsers():
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
            response = make_response(jsonify({"data":data,"message":"Logged in successfully","success":True}), 200)
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