from pymongo import MongoClient
from bson import ObjectId
from flask import Flask,render_template,jsonify,json,request
import util
import traceback
import config as cf
import time
import csv

application = Flask(__name__)

client = MongoClient(cf.DB_HOST, cf.DB_PORT)
db = client[cf.DB_NAME]


songDB.authenticate(cf.DB_USER, cf.DB_PASS)



@application.route('/')
def loadLogin():
    return render_template('content.html')

@application.route('/login', methods=['POST'])
def login():
	email = request.json['email']
	googleID = request.json['googleID']
	# print googleID
	thisMember = db.members.find_one( { "email": email } )
	if thisMember == None:
		return jsonify(status='ERROR',message=str("this user is not found"))
	db.members.update_one({'email': email},{'$set':{'profileActivated':True, 'googleID':googleID}})
	return jsonify(status='OK',message='login successful')

@application.route('/getUserProfile', methods=['POST'])
def getProfile():
	googleID = request.json['googleID']
	thisMember = db.members.find_one( { "googleID": googleID } )
	
	userDetails = dict()

	#SPECIFY ALL USEFUL INFORMATION TO BE RETURNED HERE
	userDetails["isAdmin"] = thisMember["isAdmin"]
	userDetails["leader"] = thisMember["leader"]
	userDetails["completedSurveys"] = thisMember["completedSurveys"]
	print userDetails
	return json.dumps(userDetails)

@application.route('/setSurveyCompleted', methods=['POST'])
def setSurveyCompleteStatus():
	googleID = request.json['googleID']
	db.members.update_one({"googleID": googleID}, {'$set':{'completedSurveys': True}})
	return jsonify(status='OK',message='survey status updated successful')

# @application.route('/getInactiveMembers', methods=['GET'])
# def getInactiveMembers():
# 	profiles = db.members.find( { "profileActivated": False } )
# 	names = list()
# 	for member in profiles:
# 		emails.append({member["name"]})
# 	return names


# import datetime
# def getSurveyFileName():
# 	now = datetime.datetime.now()
# 	if (now.month 
# 	print now.year, now.month, now.day, now.hour, now.minute, now.second
# 	# 2015 5 6 8 53 40


if __name__ == "__main__":
    application.debug = True
    application.run(host = cf.hostName, port = cf. portNo)
    # getInactiveMembers()