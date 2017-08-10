from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

application = Flask(__name__)

client = MongoClient('localhost:27017')
db = client.SongData

@application.route("/addSong",methods=['POST'])
def addSong():
    #future: store chords in nashville numers
    #future: send error message when collion occurs
    try:
        json_data = request.json['info']
        
        songName = json_data['songName']
        artist = json_data['artist']
        author = json_data['author']
        key = json_data['key']
        bpm = json_data['bpm']
        lyrics = json_data['lyrics']

        db.Songs.insert_one({
            'songName':songName, 
            'artist':artist, 
            'key':key, 
            'author': author, 
            'bpm': bpm, 
            'lyrics': lyrics})
        return jsonify(status='OK',message='inserted successfully')

    except Exception,e:
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
def showSongList():
    return render_template('content.html')

@application.route('/getSong',methods=['POST'])
def getSong():
    #future: retrieve song specified key, default if not specified
    try:
        songId = request.json['id']
        song = db.Songs.find_one({'_id':ObjectId(songId)})
        songDetail = {
                'songName':song['songName'],
                'artist':song['artist'],
                'id':str(song['_id']),
                'key':song['key'],
                'bpm':song['bpm'],
                'author':song['author'],
                'lyrics':song['lyrics']
                }
        return json.dumps(songDetail)
    except Exception, e:
        return str(e)

@application.route('/updateSong',methods=['POST'])
def updateSong():
    try:
        json_data = request.json['info']
        songId = json_data['id']

        songName = json_data['songName']
        artist = json_data['artist']
        author = json_data['author']
        key = json_data['key']
        bpm = json_data['bpm']
        lyrics = json_data['lyrics']

        db.Songs.update_one({'_id':ObjectId(songId)},{'$set':{
            'songName':songName, 
            'artist':artist, 
            'key':key, 
            'author': author, 
            'bpm': bpm, 
            'lyrics': lyrics}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

@application.route("/getSongList",methods=['POST'])
def getSongList():
    try:
        songs = db.Songs.find()
        
        songList = []
        for song in songs:
            print song
            songItem = {
                    'songName':song['songName'],
                    'artist':song['artist'],
                    'id': str(song['_id'])
                    }
            songList.append(songItem)
    except Exception,e:
        return str(e)
    return json.dumps(songList)


@application.route("/deleteSong",methods=['POST'])
def deleteSong():
    try:
        print(request)
        songId = request.json['id']
        db.Songs.remove({'_id':ObjectId(songId)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0', port=2000)

