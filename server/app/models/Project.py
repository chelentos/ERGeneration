from mongoengine.document import Document
from mongoengine.fields import (
  StringField,
  ObjectIdField
)

class Project(Document):
  meta = {"collection": "Projects"}
  name = StringField(required=True)
  parent = ObjectIdField(required=True)
