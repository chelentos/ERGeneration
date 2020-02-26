from pymongo import MongoClient
from collections import OrderedDict

from app.models.User import User
from werkzeug.security import generate_password_hash

from app.models.Project import Project
from app.models.Requirement import Requirement

mongo_client = MongoClient("mongodb://er-ad:t100km0201@localhost:27017/er-gen?authSource=er-gen")

if "er-gen" in mongo_client.list_database_names():
  mongo_client.drop_database("er-gen")

db = mongo_client["er-gen"]

db.create_collection("Users")

users_validator = {
  "$jsonSchema": {
      "bsonType": "object",
      "required": [ "email", "password_hash"],
      "properties": {
        "email": {
          "bsonType": "string",
          "description": "must be a string and is required"
        },
        "password_hash": {
          "bsonType": "string",
          "description": "must be a string and is required"
        },
        "isAgreeToCollectData": {
          "bsonType": "bool",
          "description": "must be a bool and is required"
        }
      }
    }
  }

query = OrderedDict([("collMod", "Users"),
        ("validator", users_validator),
        ("validationLevel", "strict")])
db.command(query)

db.create_collection("Projects")

projects_validator = {
  "$jsonSchema": {
      "bsonType": "object",
      "required": [ "name", "parent"],
      "properties": {
        "name": {
          "bsonType": "string",
          "description": "must be a string and is required"
        },
        "erd": {
          "bsonType": "object",
          "description": "must be an object and is not required"
        },
        "parent": {
          "bsonType": "objectId",
          "description": "must be an objectId and is required"
        }
      }
    }
  }

query = OrderedDict([("collMod", "Projects"),
        ("validator", projects_validator),
        ("validationLevel", "strict")])
db.command(query)

db.create_collection("Requirements")

reqs_validator = {
  "$jsonSchema": {
      "bsonType": "object",
      "required": [ "text", "req_type", "parent"],
      "properties": {
        "text": {
          "bsonType": "string",
          "description": "must be a string and is required"
        },
        "req_type": {
          "enum": [ "F", "PE", "LF", "O", "US", "SE", "A", "FT", "SC", "PO", "L", "MN" ],
          "description": "can only be one of the enum values and is required"
        },
        "parent": {
          "bsonType": "objectId",
          "description": "must be an objectId and is required"
        }
      }
    }
  }

query = OrderedDict([("collMod", "Requirements"),
        ("validator", reqs_validator),
        ("validationLevel", "strict")])
db.command(query)

u1 = User(email="test1@gmail.com", 
          password_hash=generate_password_hash("12345678", method="sha256"),
          isAgreeToCollectData=True).save()

p1 = Project(name="test_project1",
              parent=u1.id).save()

reqs = [
  {
    "text": "Система должна обновлять дисплей каждые 60 секунд.",
    "rtype": "PE"
  },
  {
    "text": "Приложение должно соответствовать цвету схемы, установленной Министерством внутренней безопасности.",
    "rtype": "LF"
  },
  {
    "text": "Продукт должен быть доступен в обычное рабочее время.",
    "rtype": "A"
  },
  {
    "text": "Система должна отображать все события в упражнении.",
    "rtype": "F"
  },
  {
    "text": "Продукт должен иметь согласованную цветовую гамму и шрифты.",
    "rtype": "LF"
  }
]

for req in reqs:
  r = Requirement(text=req["text"],
                  req_type=req["rtype"],
                  parent=p1.id).save()
