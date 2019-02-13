import pymysql
from flask import render_template, flash, redirect, url_for

from . import bp
from .forms import AddAnimalForm, AddShowForm, ViewAnimalForm, ViewShowForm, SearchUser
from ..__init__ import db
from ..utils.utils import login_required
from datetime import datetime as dt


@bp.route('/')
@login_required("ADMIN")
def admin():
    return render_template('admin/admin.html')


@bp.route('/view_visitors', methods=['GET', 'POST'])
@login_required("ADMIN")
def view_visitors():
    form = SearchUser()

    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT USERNAME, EMAIL FROM USER WHERE TYPE = 'VISITOR' AND " \
          f"(USERNAME = '{form.username.data}' or '{form.username.data}' = '') AND " \
          f"(EMAIL = '{form.email.data}' or '{form.email.data}' = '') ORDER BY {sort_by} {direction}"

    result = db.query(sql).fetchall()
    items = [{'Username': result[i][0], 'Email': result[i][1], 'Delete': 'delete_visitor/' + result[i][0]} for i in
             range(len(result))]

    return render_template('admin/view_visitors.html', form=form, items=items)


@bp.route('/delete_visitor/<string:name>', methods=['GET', 'POST'])
@login_required("ADMIN")
def delete_visitor(name):
    sql = f"DELETE FROM USER WHERE USERNAME = '{name}'"

    r = db.query(sql)

    if not isinstance(r, pymysql.cursors.Cursor):
        flash("IntegrityError", 'warning')
        return redirect(url_for('admin.view_visitors'))

    flash('Visitor deleted', 'success')

    return redirect(url_for('admin.view_visitors'))


@bp.route('/view_staff', methods=['GET', 'POST'])
@login_required("ADMIN")
def view_staff():
    form = SearchUser()

    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT USERNAME, EMAIL FROM USER WHERE TYPE = 'STAFF' AND " \
          f"(USERNAME = '{form.username.data}' or '{form.username.data}' = '') AND " \
          f"(EMAIL = '{form.email.data}' or '{form.email.data}' = '') ORDER BY {sort_by} {direction}"


    result = db.query(sql).fetchall()

    items = [{'Username': result[i][0], 'Email': result[i][1], 'Delete': 'delete_staff/' + result[i][0]} for i in
             range(len(result))]

    return render_template('admin/view_staff.html', form= form, items=items, title='View Staff')


@bp.route('/delete_staff/<string:name>')
@login_required("ADMIN")
def delete_staff(name):
    sql = f"DELETE FROM USER WHERE USERNAME = '{name}'"

    r = db.query(sql)

    if not isinstance(r, pymysql.cursors.Cursor):
        flash('IntegrityError', 'warning')
        return redirect(url_for('admin.view_staff'))

    flash('Staff deleted', 'success')

    return redirect(url_for('admin.view_staff'))


@bp.route('/view_shows', methods=['GET', 'POST'])
@login_required("ADMIN")
def view_shows():
    form = ViewShowForm.new()

    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT NAME, EXHIBIT, DATE_TIME FROM `SHOW` WHERE " \
          f"(NAME = '{form.name.data}' or '{form.name.data}' = '') AND " \
          f"(EXHIBIT = '{form.exhibit.data}' or '{form.exhibit.data}' = '') AND " \
          f"(DATE_TIME =  '{form.date.data}' or '{form.date.data}' = 'None') ORDER BY {sort_by} {direction}"

    result = db.query(sql).fetchall()

    items = [{'Name': result[i][0], 'Exhibit': result[i][1], 'Date': result[i][2],
              'Delete': 'delete_show/' + result[i][0] + '/' + str(result[i][2])} for i in range(len(result))]

    return render_template('admin/view_shows.html', form=form, items=items, title='View Shows')


@bp.route('/delete_show/<string:name>/<string:date>')
@login_required("ADMIN")
def delete_show(name, date):
    sql = f"DELETE FROM `SHOW` WHERE NAME = '{name}' AND DATE_TIME = '{date}'"

    r = db.query(sql)

    if not isinstance(r, pymysql.cursors.Cursor):
        flash('IntegrityError', 'warning')
        return redirect(url_for('admin.view_shows'))

    flash('Show deleted', 'success')

    return redirect(url_for('admin.view_shows'))


@bp.route('/view_animals', methods=['GET', 'POST'])
@login_required("ADMIN")
def view_animals():
    form = ViewAnimalForm.new()

    min_age = form.min_age.data
    max_age = form.max_age.data

    if min_age and min_age < 0:
        flash("Min must be positive", 'warning')
        return redirect(url_for("admin.view_animals"))

    if max_age and max_age < 0:
        flash("Max must be positive", 'warning')
        return redirect(url_for("admin.view_animals"))

    if (min_age and max_age) and max_age < min_age:
        flash("Max must be more than Min", 'warning')
        return redirect(url_for("admin.view_animals"))

    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT NAME, SPECIES, EXHIBIT, AGE, TYPE FROM ANIMAL WHERE " \
          f"(NAME = '{form.name.data}' or '{form.name.data}' = '') AND " \
          f"(SPECIES = '{form.species.data}' or '{form.species.data}' = '') AND " \
          f"(EXHIBIT = '{form.exhibit.data}' or '{form.exhibit.data}' = '') AND " \
          f"(AGE >= '{form.min_age.data}' or '{form.min_age.data}' = 'None') AND " \
          f"(AGE <= '{form.max_age.data}' or '{form.max_age.data}' = 'None') AND " \
          f"(TYPE =  '{form.type.data}' or '{form.type.data}' = '') ORDER BY {sort_by} {direction}"

    result = db.query(sql).fetchall()

    items = [{'Name': result[i][0], 'Species': result[i][1], 'Exhibit': result[i][2], 'Age': result[i][3],
              'Type': result[i][4], 'Delete': 'delete_animals/' + result[i][0] + '/' + result[i][1]} for i in
             range(len(result))]

    return render_template('admin/view_animals.html', form=form, items=items, title='View Animals')


@bp.route('/delete_animals/<string:name>/<string:species>')
@login_required("ADMIN")
def delete_animals(name, species):
    sql = f"DELETE FROM ANIMAL WHERE NAME = '{name}' AND SPECIES = '{species}'"

    r = db.query(sql)

    if not isinstance(r, pymysql.cursors.Cursor):
        flash('IntegrityError', 'warning')
        return redirect(url_for('admin.view_animals'))

    flash('Animal deleted', 'success')

    return redirect(url_for('admin.view_animals'))


@bp.route('/add_show', methods=['GET', 'POST'])
@login_required("ADMIN")
def add_show():
    form = AddShowForm.new()

    if form.validate_on_submit():

        date_time = str(form.date.data) + str(' ') + str(form.time.data)

        if dt.now() >= dt.strptime(date_time, '%Y-%m-%d %H:%M:%S'):
            flash(f"Cannot add show in the past", 'warning')
            return redirect(url_for('admin.add_show'))

        query = f"SELECT * FROM `SHOW` WHERE " \
                f"(HOST = '{form.staff.data}') AND " \
                f"(DATE_TIME = '{date_time}')"

        if db.query(query).fetchone():
            flash(f"{form.staff.data} is busy at {form.time.data} on the {form.date.data}", 'warning')
            return redirect(url_for('admin.add_show'))

        sql = f"INSERT INTO `SHOW` (NAME, DATE_TIME, HOST, EXHIBIT) " \
              f"VALUES ('{form.name.data}', '{date_time}', '{form.staff.data}', '{form.exhibit.data}')"

        r = db.query(sql)

        if not isinstance(r, pymysql.cursors.Cursor):
            flash("IntegrityError", 'warning')
            return redirect(url_for('admin.add_show'))
        else:
            flash("You successfully added the show", 'success')
            return redirect(url_for('admin.add_show'))

    return render_template('admin/add_show.html', form=form, title='Add Show')


@bp.route('/add_animal', methods=['GET', 'POST'])
@login_required("ADMIN")
def add_animal():
    form = AddAnimalForm.new()
    if form.validate_on_submit():

        sql = f"INSERT INTO ANIMAL (NAME, SPECIES, TYPE, AGE, EXHIBIT) " \
              f"VALUES ('{form.name.data}', '{form.species.data}', '{form.type.data}', " \
              f"'{form.age.data}', '{form.exhibit.data}')"

        r = db.query(sql)

        if not isinstance(r, pymysql.cursors.Cursor):
            flash("IntegrityError", 'warning')
            return redirect(url_for('admin.add_animal'))
        else:
            flash("You successfully added the animal", 'success')
            return redirect(url_for('admin.add_animal'))

    return render_template('admin/add_animal.html', form=form, title='Add Animal')
