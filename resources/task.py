from models.db import db
from models.task import Task
from models.user import User
from flask_restful import Resource
from flask import request


class Tasks(Resource):
    def get(self):
        tasks = Task.find_all()
        return tasks

    def post(self):
        data = request.get_json()
        params = {}
        for k in data.keys():
            params[k] = data[k]
        task = Task(**params)
        task.create()
        return task.json(), 201


class TaskDetail(Resource):
    def get(self, task_id):
        pass

    def put(self, task_id):
        data = request.get_json()
        task = Task.find_by_id(task_id)
        for k in data.keys():
            task[k] = data[k]
        db.session.commit()
        return task.json()

    def delete(self, task_id):
        task = Task.find_by_id()
        if not task:
            return {"msg": "Not found"}, 404
        db.session.delete(task)
        db.session.commit()
        return {"msg": "Task Deleted", "payload": task_id}
