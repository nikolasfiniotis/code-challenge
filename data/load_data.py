import requests
import pymongo

url = "https://api.nobelprize.org/v1/prize.json"
response = requests.get(url)
data = response.json()

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["nobel"]
collection = db["prizes"]

collection.drop()
collection.insert_many(data["prizes"])
