from mongoengine.document import Document
from mongoengine.fields import (
  StringField,
  DictField,
  ObjectIdField
)

class Project(Document):
  meta = {"collection": "Projects"}
  name = StringField(required=True)
  erd = DictField(required=False)
  parent = ObjectIdField(required=True)
