from pymongo import MongoClient
from flask import Flask,render_template,jsonify,json,request
import util
import traceback
import os
import time

application = Flask(__name__)

hostName = '0.0.0.0'
portNo = int(os.environ.get("PORT", 5000))

DB_NAME = heroku_9trbkmfx  
DB_HOST = ds161262.mlab.com
DB_PORT = 61262
DB_USER = ericthuang 
DB_PASS = songcloud1234

client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]
db.authenticate(DB_USER, DB_PASS)



@application.route("/addSong",methods=['POST'])
def addSong():
    #use milli_time to create unique ID for recalling song and compress to hex string
    unqID = str(hex(int(round(time.time() * 1000)))).replace("0x", "")

    try:
        json_data = request.json['info']
        
        try:
            songName = json_data['songName']
        except:
            songName = " "
        try:
            artist = json_data['artist']
        except:
            artist = " "
        try:
            author = json_data['author']
        except:
            author = " "
        try:
            key = json_data['key']
        except:
            key = " "
        try:
            bpm = json_data['bpm']
        except:
            bpm = " "

        songID = songDB.Songs.insert_one({
            'songName':songName, 
            'artist':artist, 
            'key':key, 
            'author': author, 
            'bpm': bpm, 
            'lyrics': {},
            'chords': {}, 
            'IDKEY': unqID})

        song = songDB.Songs.find_one({'IDKEY':unqID})

        songID = str(song['_id'])

        try:
            URL = "http://" + str(hostName) + ":" + str(portNo) +  "/" + str(song['IDKEY'])
        except:
            URL = "url not available"

        songDetail = {
                'songName':songName,
                'artist':artist,
                'id':songID,
                'key':key,
                'bpm':bpm,
                'displayedKey': key,
                'URL': URL
                }
        return json.dumps(songDetail)

    except Exception,e:
        print(str(e))
        traceback.print_exc()
        return jsonify(status='ERROR',message=str(e))

@application.route('/')
def showSongList():
    return render_template('content.html')

@application.route('/getSong',methods=['POST'])
def getSong():
    #future: retrieve song specified key, default if not specified
    try:
        songID = request.json['id']
        song = songDB.Songs.find_one({'_id':ObjectId(songID)})

        try:
            songName = song['songName']
        except:
            songName = " "
        try:
            artist = song['artist']
        except:
            artist = " "
        try:
            author = song['author']
        except:
            author = " "
        try:
            key = song['key']
        except:
            key = " "

        try: #for updating key
            desiredKey = request.json['selectedKey']
        except:
            desiredKey = key

        try:
            bpm = song['bpm']
        except:
            bpm = " "
        try:
            lyrics = util.getPrettified_Lyrics(song['lyrics'])
        except:
            lyrics = ""

        linesCount = len(lyrics.split('\n')) - 1
        try:
            chords = util.getPrettified_Chords(song['chords'], linesCount , key, desiredKey)
        except:
            chords = (util.pad(" ", 64) * linesCount)

        songID = str(song['_id'])

        try:
            URL = "http://" + str(hostName) + ":" + str(portNo) +  "/" + str(song['IDKEY'])
        except:
            URL = "url not available"

        songDetail = {
                'songName':songName,
                'artist':artist,
                'id':songID,
                'key':key,
                'bpm':bpm,
                'displayedKey': desiredKey, 
                'author':author,
                'lyrics':lyrics,
                'chords': chords, 
                'URL': URL
                }
        return json.dumps(songDetail)
    except Exception, e:
        print(str(e))
        traceback.print_exc()
        return str(e)

@application.route('/<IDKEY>')
def getSongByID(IDKEY):
    #future: retrieve song specified key, default if not specified
    try:
        song = songDB.Songs.find_one({'IDKEY': IDKEY})

        try:
            songName = song['songName']
        except:
            songName = " "
        try:
            artist = song['artist']
        except:
            artist = " "
        try:
            author = song['author']
        except:
            author = " "
        try:
            key = song['key']
        except:
            key = " "

        try: #for updating key
            desiredKey = request.json['selectedKey']
        except:
            desiredKey = key

        try:
            bpm = song['bpm']
        except:
            bpm = " "
        try:
            lyrics = util.getPrettified_Lyrics(song['lyrics'])
        except:
            lyrics = ""

        linesCount = len(lyrics.split('\n')) - 1
        try:
            chords = util.getPrettified_Chords(song['chords'], linesCount , key, desiredKey)
        except:
            chords = (util.pad(" ", 64) * linesCount)

        songID = str(song['_id'])

        try:
            URL = "http://" + str(hostName) + ":" + str(portNo) +  "/" + str(song['IDKEY'])
        except:
            URL = " "

        songDetail = {
                'songName':songName,
                'artist':artist,
                'id':songID,
                'key':key,
                'bpm':bpm,
                'displayedKey': desiredKey, 
                'author':author,
                'lyrics':lyrics,
                'chords': chords,
                'URL': URL
                }
        return render_template('content.html', currentSong = json.dumps(songDetail))

    except Exception, e:
        print(str(e))
        traceback.print_exc()
        return str(e)

@application.route('/getRawChords',methods=['POST'])
def getRawChords():
    try:
        songID = request.json['id']
        song = songDB.Songs.find_one({'_id':ObjectId(songID)})

        chords = song['chords']

        chordDetail = {'chords': chords}

        return json.dumps(chordDetail)
    except Exception, e:
        print(str(e))
        traceback.print_exc()
        return str(e)

@application.route('/updateSong',methods=['POST'])
def updateSong():
    try:
        json_data = request.json['info']
        songID = json_data['id']
        song = songDB.Songs.find_one({'_id':ObjectId(songID)})

        songName = json_data['songName']
        artist = json_data['artist']
        # author = json_data['author']
        key = json_data['key']
        # bpm = json_data['bpm']

        lyrics = util.lyricFormatToStore(json_data['lyrics'])

        songDB.Songs.update_one({'_id':ObjectId(songID)},{'$set':{
            'songName':songName, 
            'artist':artist, 
            'key':key, 
            # 'author': author, 
            # 'bpm': bpm, 
            'lyrics': lyrics}})
        return jsonify(status='OK',message='updated successfully')
    except Exception, e:
        print(str(e))
        traceback.print_exc()
        return jsonify(status='ERROR',message=str(e))

@application.route('/checkChordExistsHere',methods=['POST'])
def checkChordExistsHere():
    try:
        json_data = request.json['info']
        songID = json_data['songID']
        song = songDB.Songs.find_one({'_id':ObjectId(songID)})
        chords = song['chords']

        position = int(json_data['position'].replace("char", "").strip()) - 1 #cuz it starts at 1

        # position_D = util.decompressPosition(position + 1)
        # row = position_D[0]
        # col = position_D[1]

        try:
            if(len(chords[str(position)]) != 0):
                #check if chord word tail from another chord exists here














                return(json.dumps({"status": True}))
            else:
                return(json.dumps({"status": False}))

        except Exception, f:
            return(json.dumps({"status": False}))

    except Exception, e:
        traceback.print_exc()
        return jsonify(status='ERROR',message=str(e))
    return jsonify(status='OK',message='')

@application.route('/removeChord',methods=['POST'])
def removeChord():
    try:
        json_data = request.json['info']
        songID = json_data['songID']
        song = songDB.Songs.find_one({'_id':ObjectId(songID)})
        chords = song['chords']

        position = int(json_data['position'].replace("char", "").strip()) - 1 #cuz it starts at 1

        chords.pop(str(position), None)

        # remove this chord from db
        songDB.Songs.update_one({'_id':ObjectId(songID)}, {"$set": {"chords": chords}});
        
    except Exception, e:
        traceback.print_exc()
        return jsonify(status='ERROR',message=str(e)) 
    return jsonify(status='OK',message='chord removed successfully')

@application.route('/insertChord',methods=['POST'])
def putChord():
    try:
        json_data = request.json['info']

        key = json_data['key']
        songID = json_data['songID']
        position = int(json_data['position'].replace("char", "").strip()) - 1 #cuz it starts at 1
        
        #identify key someday
        chord = json_data['chord']

        song = songDB.Songs.find_one({'_id':ObjectId(songID)})
        try:
            chords = song['chords']
        except: #reinitialize to empty
            chords = list()



        # // make sure index + len(chordword) is free


        # push to db
        chordData = [position, key, chord] #store as list of data
        songDB.Songs.update_one({'_id':ObjectId(songID)}, {"$set": {'chords.' + str(position): chord}});

        return jsonify(status='OK',message='chord inserted successfully')
    except Exception, e:
        print(str(e))
        traceback.print_exc()
        return jsonify(status='ERROR',message=str(e))


@application.route("/getSongList",methods=['POST'])
def getSongList():
    try:
        songs = songDB.Songs.find()
        
        songList = []
        for song in songs:
            # print song
            songItem = {
                    'songName':song['songName'],
                    'artist':song['artist'],
                    'id': str(song['_id'])
                    }
            songList.append(songItem)
    except Exception,e:
        print(str(e))
        traceback.print_exc()
        return str(e)
    return json.dumps(songList)


@application.route("/deleteSong",methods=['POST'])
def deleteSong():
    try:
        # print(request)
        songID = request.json['id']
        songDB.Songs.remove({'_id':ObjectId(songID)})
        return jsonify(status='OK',message='deletion successful')
    except Exception, e:
        print(str(e))
        traceback.print_exc()
        return jsonify(status='ERROR',message=str(e))

if __name__ == "__main__":
    application.debug = True
    application.run(host=hostName, port=portNo)

