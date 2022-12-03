# Python Flask Associations

![](https://i0.wp.com/blog.fossasia.org/wp-content/uploads/2018/05/Blog-Post-2-1.png?fit=828%2C315&ssl=1)

## Overview

In this exercise, we'll learn how define and query relationships with `Flask` and `Flask SQLAlchemy`. We'll be focusing solely on defining and querying these records. We'll only be implementing a `one-many` relationship as you can take this knowledge and implement `many-many`.

## Getting Started

- Fork and Clone
- MacOS: `virtualenv venv` | WSL: `python3 -m venv venv`
- `source venv/bin/activate`
- `pip3 install -r requirements.txt`

## Instructions

In order to get our application going, we'll first need to do a few things:

- Create our database
  - `createdb flask_assocs`
- Next we'll need to set up and run our migrations
  - `flask db init`
  - `flask db upgrade`

### Defining Relationships

Now that our database is created and the tables are up to date, we'll start with defining our associations. You've been provided with two models, `User`,`Task`. The relationships are as follows:

- _User has-many Task_
- _Task belongs-to User_

Let's start with the `Task` model.

### Belongs To

Open `models/task.py`.

We first need to define a `Foreign Key` that will reference a record in the `users` table.

In the section where the columns are defined, add the following:

```py
 user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
```

With the above line, we're creating a `user_id` field in the `tasks` table and defining it as a foreign key.

Next we need to give our `Task` a `user` property which will allow us to retrieve a user if needed. Add the following to the `Task` model. It may be worthwhile to make this the last entry for the list of fields.

```py
user = db.relationship("User", back_populates="tasks")
```

This line tells the `Task` model about it's relationship to the `User`. It's the equivalent of `Sequelizes'` `belongsTo` method.

You can read more about this **[Here](https://rb.gy/p5qnnt)**.

## Has Many

Now that we've set up the `Foreign Key` on our `Task` model, we can tell the `User` model how they're associated. Head over to `models/user.py`.

Let's add the following line to the bottom of the attributes for our `User` model:

```py
tasks = db.relationship("Task", cascade='all', back_populates="user")
```

Take notice that here we are using `tasks` as the property. This is so we can read our code and understand what kind of relationship this should be. When querying for tasks belonging to a user, we want to have a list being returned.

Also notice that we are also providing a `cascade` option here. This ensures that if we delete a user from our database, their associated tasks are also removed automatically.

## Updating Our Database

Now that we've added a foreign key to our `Task` model, we need to create a new migration to update our `tasks` table:

```sh
flask db migrate -m "associate user-task"
```

Next we'll run the new migration:

```sh
flask db upgrade
```

It's a good idea to check your tables manually just to ensure that the migration was successful:

```sh
psql flask_assocs
```

```sql
SELECT * FROM tasks;
```

## Querying Data

Resources have been created for you. Take a look at `app.py` for the endpoints and the corresponding endpoints.

We'll start with getting tasks for a specific user. Find the `get` method in the `UserDetail` class located in `resources/user.py`

We'll want to query for a specific user by id and include their tasks. Start by importing `joinedload` from `SQL Alchemy` at the top of the file:

```py
from sqlalchemy.orm import joinedload
```

Next we'll set up the query that will find a specific user and load in the associated tasks.

Add the following to the `get` method:

```py
user = User.query.options(joinedload('tasks')).filter_by(id=user_id).first()
```

With the `joinedload` option we can now access the users tasks by using `dot` notation:

```py
user.tasks
```

Only one problem... The list of tasks returned are not in a json serialized format. Lucky for us, because the the list of tasks in an instance of the `Task` model, we can use the `.json()` method created for your to format the data.

Add the following:

```py
tasks = [t.json() for t in user.tasks]
```

Now we're ready to send the response back. We can use the `spread` operator here to return a dictionary with the user converted to json and the list of tasks.

```py
return {**user.json(), "tasks": tasks}
```

At this point, our `User` and `UserDetail` resources are ready to go. Start up your flask server with `python3 app.py`. Use insomnia to create a new user.

### Creating Tasks

Once you have a user successfully created, we can start creating some tasks.

Create a few tasks using the newly created users' id.

The request body should follow the following format:

```json
{
  "content": "<str>",
  "user_id": "<int>"
}
```

Now that we've created a few tasks, we're ready to try retrieving them. Open the `resources/task.py` file and find the `get` method within `TaskDetail`.

Using your new knowledge of querying joined records, build in the functionality to display a specific tasks' user along with the task you are querying for.

### Api Testing

Once you've successfully retrieved the user and task, test the rest of the endpoints and functionality. Keep checking your database and observe what happens when you delete a user.

## Recap

In this lab, we learned how define and query relationships using Flask and SQLAlchemy. We utilized the `joinedload` option from the `SQLAlchemy` orm to help us in loading the data required.

## Resources

- [SQL Alchemy Relationships](https://bit.ly/2OZVi9d)
- [SQL Alchemy Relationship Loading](https://bit.ly/3vWgiyh)
