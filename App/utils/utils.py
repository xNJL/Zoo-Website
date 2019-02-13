from functools import wraps
from flask_login import current_user
from flask import current_app

from ..__init__ import db


def login_required(role="VISITOR"):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()

            user_type = current_user.get_user_type()
            if user_type != role:
                return current_app.login_manager.unauthorized()

            return f(*args, **kwargs)

        return decorated_view

    return wrapper


def get_exhibit_choices():
    sql = "SELECT DISTINCT NAME FROM EXHIBIT"
    result = db.query(sql).fetchall()

    choices = [('', '')]
    choices.extend([(result[i][0], result[i][0]) for i in range(len(result))])

    return choices


def get_animal_type_choices():
    sql = "SELECT DISTINCT TYPE FROM ANIMAL"
    result = db.query(sql).fetchall()

    choices = [('', '')]
    choices.extend([(result[i][0], result[i][0]) for i in range(len(result))])

    return choices


def get_staff_choices():
    sql = "SELECT DISTINCT USERNAME FROM STAFF"
    result = db.query(sql).fetchall()

    choices = [('', '')]
    choices.extend([(result[i][0], result[i][0]) for i in range(len(result))])

    return choices
