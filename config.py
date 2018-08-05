import os

'''for heroku'''
hostName = 'localhost'
portNo = int(os.environ.get("PORT", 5000))

DB_NAME = "heroku_jzbkv8xb"
DB_HOST = "ds213612.mlab.com"
DB_PORT = 13612
DB_USER = "heroku_jzbkv8xb" 
DB_PASS = "5l1t80k64m5tmta14o8q7dkqo6"

'''for local'''
# hostName = 'localhost'
# portNo = 2000

# DB_NAME = "IgniteWorship"
# DB_HOST = "localhost"
# DB_PORT = 27017