#!flask/bin/python
from flask import Flask, jsonify ,render_template,redirect
import sqlite3
from flask import g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
import json

app = Flask(__name__)
#innitliaze DB
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)
#create Model
class Suggestions(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    suggestion1=db.Column(db.String(500),nullable=False)
    suggestion2=db.Column(db.String(500),nullable=False)
    suggestion3=db.Column(db.String(500),nullable=False)
    suggestion4=db.Column(db.String(500),nullable=False)
    suggestion5=db.Column(db.String(500),nullable=False)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
    updated_at=db.Column(db.DateTime,default=datetime.utcnow)


#create a function 
def __repr__(self):
    return '<Name %r>' % self.id

@app.route('/', methods=['GET','POST'])
def get_tasks():
    # return jsonify({'tasks': tasks})
    allSuggestions=Suggestions.query.order_by(Suggestions.created_at)
    return render_template('index.html',allSuggestions=allSuggestions)


@app.route('/submitForm',methods=['POST','GET'])
def submitForm():
    print("**************************************")
    if request.method== "POST":
        #fetch values from post form 
        inputFromForm=request.form['text']
        print(inputFromForm)
        #save to db 
        try:
            newSuggestionObject=Suggestions(suggestion1="suggesttion1",suggestion2="suggesttion2",suggestion3="suggesttion3",suggestion4="suggesttion4",suggestion5="suggesttion5")
            db.session.add(newSuggestionObject)
            db.session.commit()
            print("--success -- created -- model")
            return redirect("/")
        except Exception as e:
            print("Error occured while saving to database")
            print(e)
            return redirect("/")
    else:
        return redirect("/")


@app.route('/ajax',methods=['GET'])
def servreAjax():
    if request.method=='GET':
        try:
           
            print( request.args)
            print("AJAX REQUEST RECIEVED ")
            return jsonify({'tasks': {"name":"ahmed"}})
        except Exception as e:
            print("AJAX REQUEST RECIEVED --Excepption ")
            print(e)
            return jsonify({'tasks': {"name":"exception occurred"}})


if __name__ == '__main__':
    app.run(debug=True)