from pymongo import MongoClient
from decouple import config

# Local Conection
# db_client = MongoClient().local 

# Cloud Conection
# db_client = MongoClient("mongodb+srv://user:password@cluster0.p4map19.mongodb.net/?retryWrites=true&w=majority").test

# Cloud Conection using .env
try:
    db_client = MongoClient(config("MONGO_DB")).test
    print("Database connection established")
except:
    print("Wrrong Database connection")