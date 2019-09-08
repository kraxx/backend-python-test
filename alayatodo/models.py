from alayatodo import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

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

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return '<Todo %r>' % self.description
