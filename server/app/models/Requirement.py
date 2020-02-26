from mongoengine.document import Document
from mongoengine.fields import (
  StringField,
  ObjectIdField
)

class Requirement(Document):
  meta = {"collection": "Requirements"}
  text = StringField(required=True)
  req_type = StringField(required=True)
  parent = ObjectIdField(required=True)
