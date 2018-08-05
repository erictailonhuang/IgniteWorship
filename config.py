import os

'''for heroku'''
hostName = '0.0.0.0'
portNo = int(os.environ.get("PORT", 5000))

DB_NAME = "heroku_jzbkv8xb"
DB_HOST = "ds213612.mlab.com"
DB_PORT = 13612
DB_USER = "huangeric" 
DB_PASS = "IgniteWorship1234"

'''for local'''
# hostName = 'localhost'
# portNo = 2000

# DB_NAME = "IgniteWorship"
# DB_HOST = "localhost"
# DB_PORT = 27017