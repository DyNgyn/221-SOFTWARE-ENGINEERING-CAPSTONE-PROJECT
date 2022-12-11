from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://dbadmin:H9kGaW0KH3wV1zpi@cluster0.sfcugwr.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
db=client["WebDB"]
content = db["Content"]
all_data = content.find({})
for data in all_data:
    print(data)

from app import app
if __name__ == "__main__":
    app.run(debug=True)