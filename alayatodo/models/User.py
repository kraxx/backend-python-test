import binascii
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
        Not called in our code as we do not create users, but shows how the hashing is done.

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
        Verifies a user login by comparing the provided password with the stored one using cool hashing algos.

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
