from mongoengine.document import Document
from mongoengine.fields import (
  StringField,
  DictField,
  ObjectIdField
)

class ER(Document):
  meta = {"collection": "Ers"}
  name = StringField(required=True)
  erd = DictField()
  parent = ObjectIdField(required=True)
