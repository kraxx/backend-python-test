from flask import jsonify
from flask_sqlalchemy import Pagination

from alayatodo import app, db


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
        """
        Uses SQLAlchemy's builtin pagination tools to return paginated queries

        :param page: target page number
        :return: flask_sqlalchemy.Pagination object for use in views
        """
        return cls.query.paginate(
            page=page,
            per_page=app.config.get('PAGE_ITEM_LIMIT', 5),
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
