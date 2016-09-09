from mongoengine import *
from django.conf import settings
from django.utils import timezone
from passlib.hash import pbkdf2_sha256


class Address(EmbeddedDocument):
    country = StringField()
    state = StringField()
    city = StringField()
    neighbourhood = StringField()
    street = StringField()
    number = StringField()
    complement = StringField()
    reference = StringField()


class Company(DynamicDocument):
    name = StringField(required=True)
    address = EmbeddedDocumentField(Address)
    workers = ListField(ReferenceField('User'))


class Hotel(DynamicDocument):
    head_office = ReferenceField(Company)
    address = EmbeddedDocumentField(Address)
    rating = IntField()


class User(DynamicDocument):
    email = EmailField(required=True)
    password = StringField(max_length=256)
    first_name = StringField(max_length=128)
    last_name = StringField(max_length=128)
    token = StringField(max_length=320, unique=True)
    is_active = BooleanField(required=True, default=True)
    created = DateTimeField(required=True)
    updated = DateTimeField(required=True)

    meta = {"allow_inheritance": True}

    def __str__(self):
        return self.email

    def set_password(self, password):
        self.password = pbkdf2_sha256.encrypt(password,
                                              rounds=settings.HASH_ROUNDS,
                                              salt_size=settings.HASH_SALT_SIZE)

    def generate_token(self):
        data = {
            "created": timezone.now().strftime('%Y%m%d%H%M%S'),
            "id": str(self.id),
            "email": self.email,
            "full_name": "{} {}".format(self.first_name, self.last_name),
        }
        return str(settings.TOKEN_MANAGER.make_token(data))

    def refresh_token(self):
        self.token = self.generate_token()
        self.save()
        return self.token

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        if not self.token:
            self.token = self.refresh_token()
        self.updated = timezone.now()
        super(User, self).save(*args, **kwargs)


class Client(User):
    address = EmbeddedDocumentField(Address)


class Worker(User):
    roles = ListField(StringField())
    is_manager = BooleanField(required=True, default=False)
    company = ReferenceField(Company)
