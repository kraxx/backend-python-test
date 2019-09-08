import binascii
from flask import jsonify
from flask_sqlalchemy import Pagination
import hashlib
import os

from alayatodo import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    @classmethod
    def get(cls, username: str) -> object:
        return cls.query.filter_by(username=username).first()

    def hash_password(self) -> str:
        """
        Hashes a plaintext password using SHA256 with a randomly generated salt
        Does not get called in our code as we do not create users, but shows how the hashing is done.

        ref:
        https://www.vitoshacademy.com/hashing-passwords-in-python/
        """
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      self.password.encode('utf-8'),
                                      salt,
                                      100000
                                      )
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify(self, provided_password: str) -> bool:
        """
        :param provided_password: plaintext password provided in login form
        :return: True if provided_password matches the hashed stored password
        """
        salt = self.password[:64]
        stored_password = self.password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000
                                      )
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def __repr__(self) -> str:
        return '<User %r>' % self.username


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id: str, description: str) -> None:
        self.user_id = user_id
        self.description = description

    @classmethod
    def get(cls, id: int) -> object:
        return cls.query.filter_by(id=id).first()

    @classmethod
    def add(cls, user_id: str, description: str) -> None:
        todo = cls(user_id, description)
        db.session.add(todo)
        db.session.commit()

    @classmethod
    def delete(cls, id: int) -> None:
        todo = cls.get(id)
        db.session.delete(todo)
        db.session.commit()

    @classmethod
    def toggle_completion(cls, id: int) -> None:
        todo = cls.get(id)
        todo.completed = not todo.completed
        db.session.commit()

    @classmethod
    def paginate(cls, page: int) -> Pagination:
        return cls.query.paginate(
            page=page,
            per_page=5,
            error_out=False
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'user_id': self.user_id
        }

    def json(self) -> str:
        return jsonify(self.to_dict())

    def __repr__(self) -> str:
        return '<Todo %r>' % self.description
