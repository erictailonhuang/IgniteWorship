import os

'''for heroku'''
hostName = '0.0.0.0'
portNo = int(os.environ.get("PORT", 5000))

DB_NAME = "heroku_9trbkmfx"
DB_HOST = "ds161262.mlab.com"
DB_PORT = 61262

'''for local'''
# hostName = '0.0.0.0'
# portNo = 2000

# DB_NAME = "SongData"
# DB_HOST = "localhost"
# DB_PORT = 27017