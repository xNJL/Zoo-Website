from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from . import bp
from .forms import LoginForm, RegistrationForm
from .. import login
from ..__init__ import db
from ..model.User import User

USER_TYPE = {0: 'VISITOR', 1: 'STAFF'}


@login.user_loader
def load_user(email):
    sql = f"SELECT USERNAME, TYPE, PASSWORD_HASH FROM fake_db.USER WHERE EMAIL ='{email}'"
    result = db.query(sql).fetchone()

    if not result:
        return None

    user = User(username=result[0], email=email, user_type=result[1])
    return user


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == "ADMIN":
            return redirect(url_for('admin.admin'))

        elif current_user.user_type == "STAFF":
            return redirect(url_for('staff.staff'))

        elif current_user.user_type == "VISITOR":
            return redirect(url_for('visitor.visitor'))

    form = LoginForm()
    if form.validate_on_submit():

        sql = f"SELECT USERNAME, TYPE, PASSWORD_HASH FROM fake_db.USER WHERE EMAIL ='{form.email.data}'"
        result = db.query(sql).fetchone()

        if result is None:
            flash('Invalid mail or password', 'warning')
            return redirect(url_for('auth.login'))

        user = User(email=form.email.data, username=result[0], user_type=result[1], password_hash=result[2])
        # user.set_password(form.password.data)

        if user is None or not user.check_password(form.password.data):
            flash('Invalid mail or password', 'warning')
            return redirect(url_for('auth.login'))

        login_user(user)

        if user.user_type == "ADMIN":
            return redirect(url_for('admin.admin'))

        elif user.user_type == "STAFF":
            return redirect(url_for('staff.staff'))

        elif user.user_type == "VISITOR":
            return redirect(url_for('visitor.visitor'))

    return render_template('auth/login.html', form=form, title='Login')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        if current_user.user_type == "ADMIN":
            return redirect(url_for('admin.admin'))

        elif current_user.user_type == "STAFF":
            return redirect(url_for('staff.staff'))

        elif current_user.user_type == "VISITOR":
            return redirect(url_for('visitor.visitor'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, user_type=USER_TYPE[int(form.user_type.data)])
        user.set_password(form.password.data)

        sql = f"INSERT INTO fake_db.USER (USERNAME , EMAIL , TYPE , PASSWORD_HASH) " \
              f"VALUES ( '{user.username}', '{user.email}', '{user.user_type}', '{user.password_hash}')"
        db.query(sql)
        if user.user_type == 'STAFF':
            sql = f"INSERT INTO fake_db.STAFF (USERNAME) " \
                  f"VALUES ( '{user.username}')"
        else:
            sql = f"INSERT INTO fake_db.VISITOR (USERNAME) " \
                  f"VALUES ( '{user.username}')"
        db.query(sql)
        flash(f'Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')
