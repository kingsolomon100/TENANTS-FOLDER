from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

username = urllib.parse.quote_plus("kingsman")
password = urllib.parse.quote_plus("soli.1234")

uri = f"mongodb+srv://{username}:{password}@solibaba.ddkew18.mongodb.net/?appName=solibaba"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Access the database
db = client["My-backend-Blog"]

# Access the collection
# userfile = db["Userfile"]
# Blog = db["Blog"]
# Otp_collection = db["Otp_collection"]
tenants = db['tenants'] 


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!") 
except Exception as e:
    print("Failed to connected to the database")
    print(e)