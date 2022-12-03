from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from models.db import db
from models import user,task
from resources import user, task

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost:5432/flask_assocs"
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app,db)

api.add_resource(user.Users, '/users')
api.add_resource(user.UserDetail, '/users/<int:user_id>')
api.add_resource(task.Tasks, '/tasks')
api.add_resource(task.TaskDetail,'/tasks/<int:task_id>')
if __name__ == '__main__':
    app.run(debug=True)
