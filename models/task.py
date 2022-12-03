from datetime import datetime
from models.db import db


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(
    ), nullable=False, onupdate=datetime.utcnow)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

    def json(self):
        return {"id": self.id, "content": self.content, "user_id": self.user_id, "created_at": str(self.created_at), "updated_at": str(self.updated_at)}

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_all(cls):
        tasks = Task.query.all()
        return [t.json() for t in tasks]

    @classmethod
    def find_by_id(cls, task_id):
        task = Task.query.filter_by(id=task_id).first()
        return task
