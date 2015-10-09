from datetime import datetime
from mongoengine import *


class Member(Document):
    username = StringField(unique=True)
    email = EmailField()
    name = StringField()
    created_on = DateTimeField(default=datetime.now())


class ProfileMember(Document):
    user = ReferenceField('Member', reverse_delete_rule=CASCADE)
    name = StringField(max_length=50)
    email = EmailField()
    address = StringField()
    created_on = DateTimeField(default=datetime.now())
