from flask import render_template, flash, redirect, url_for
from datetime import datetime as dt

from . import bp
from .forms import ViewShowHistoryForm, ViewExhibitHistoryForm, SearchShowForm, SearchAnimalForm, SearchExhibitForm, \
    ExhibitDetail
from ..__init__ import db
from ..utils.utils import login_required
from flask_login import current_user
import pymysql

WATER = {0: 'No', 1: 'Yes'}


@bp.route('/')
@login_required("VISITOR")
def visitor():
    return render_template('visitor/visitor.html')


@bp.route('/search_exhibit', methods=['GET', 'POST'])
@login_required("VISITOR")
def search_exhibit():
    form = SearchExhibitForm()

    min_animal = form.min_animal.data
    max_animal = form.max_animal.data

    if min_animal and min_animal < 0:
        flash("Min must be positive", 'warning')
        return redirect(url_for("visitor.search_exhibit"))

    if max_animal and max_animal < 0:
        flash("Max must be positive", 'warning')
        return redirect(url_for("visitor.search_exhibit"))

    if (min_animal and max_animal) and max_animal < min_animal:
        flash("Max must be more than Min", 'warning')
        return redirect(url_for("visitor.search_exhibit"))

    min_size = form.min_size.data
    max_size = form.max_size.data

    if min_size and min_size < 0:
        flash("Min must be positive", 'warning')
        return redirect(url_for("visitor.search_exhibit"))

    if max_size and max_size < 0:
        flash("Max must be positive", 'warning')
        return redirect(url_for("visitor.search_exhibit"))

    if (min_size and max_size) and max_size < min_size:
        flash("Max must be more than Min", 'warning')
        return redirect(url_for("visitor.search_exhibit"))

    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT * FROM (SELECT " \
          f"EXHIBIT.NAME, EXHIBIT.SIZE, EXHIBIT.WATER, COUNT(*) AS C FROM EXHIBIT LEFT JOIN ANIMAL ON (EXHIBIT.NAME = ANIMAL.EXHIBIT) WHERE " \
          f"(EXHIBIT.NAME = '{form.name.data}' or '{form.name.data}' = '') AND " \
          f"(EXHIBIT.SIZE >= '{form.min_size.data}' or '{form.min_size.data}' = 'None') AND " \
          f"(EXHIBIT.SIZE <= '{form.max_size.data}' or '{form.max_size.data}' = 'None') AND " \
          f"(EXHIBIT.WATER =  '{form.water.data}' or '{form.water.data}' = '')" \
          f"GROUP BY EXHIBIT.NAME) AS T " \
          f"WHERE (C >= '{form.min_animal.data}' or '{form.min_animal.data}' = 'None') AND " \
          f"(C <= '{form.max_animal.data}' or '{form.max_animal.data}' = 'None') ORDER BY {sort_by} {direction}"

    result = db.query(sql).fetchall()
    items = [{'Name': result[i][0], 'Size': result[i][1], 'Water': WATER[result[i][2]], 'Number of Animals': result[i][3], 'Link': 'exhibit_detail/'+result[i][0]} for i in
             range(len(result))]

    return render_template('visitor/search_exhibit.html', form=form, items=items, title='Search Exhibit')


@bp.route('/view_exhibit_history', methods=['GET', 'POST'])
@login_required("VISITOR")
def view_exhibit_history():
    form = ViewExhibitHistoryForm()

    min_visits = form.min_visits.data
    max_visits = form.max_visits.data

    if min_visits and min_visits < 0:
        flash("Min must be positive", 'warning')
        return redirect(url_for("visitor.view_exhibit_history"))

    if max_visits and max_visits < 0:
        flash("Max must be positive", 'warning')
        return redirect(url_for("visitor.view_exhibit_history"))

    if (min_visits and max_visits) and max_visits < min_visits:
        flash("Max must be more than Min", 'warning')
        return redirect(url_for("visitor.view_exhibit_history"))

    username = current_user.username
    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT A.EXHIBIT, DATE_TIME, C FROM (SELECT EXHIBIT, DATE_TIME FROM VISIT_EXHIBIT WHERE VISITOR='{username}') AS A" \
          f" LEFT JOIN " \
          f"(SELECT EXHIBIT, COUNT(*) AS C FROM VISIT_EXHIBIT WHERE VISITOR='{username}' GROUP BY EXHIBIT) AS B " \
          f"ON (A.EXHIBIT=B.EXHIBIT) WHERE" \
          f"(A.EXHIBIT = '{form.name.data}' or '{form.name.data}' = '') AND " \
          f"(A.DATE_TIME = '{form.date.data}' or '{form.date.data}' = 'None') AND " \
          f"(C <= '{form.max_visits.data}' or '{form.max_visits.data}' = 'None') AND " \
          f"(C >= '{form.min_visits.data}' or '{form.min_visits.data}' = 'None') ORDER BY {sort_by} {direction}"

    result = db.query(sql).fetchall()
    items = [{'Name': result[i][0], 'Time': result[i][1], 'Number of Visits': result[i][2], 'Link':'exhibit_detail/'+result[i][0]} for i in range(len(result))]

    return render_template('visitor/view_exhibit_history.html', form=form, items=items, title='View Exhibit History')


@bp.route('/search_show', methods=['GET', 'POST'])
@login_required("VISITOR")
def search_show():
    form = SearchShowForm.new()
    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT NAME, DATE_TIME, EXHIBIT FROM `SHOW` WHERE " \
          f"(NAME = '{form.name.data}' or '{form.name.data}' = '') AND " \
          f"(date(DATE_TIME) = '{form.date.data}' or '{form.date.data}' = 'None') AND " \
          f"(EXHIBIT = '{form.exhibit.data}' or '{form.exhibit.data}' = '') ORDER BY {sort_by} {direction}"
    result = db.query(sql).fetchall()
    items = [{'Name': result[i][0], 'Exhibit': result[i][2], 'Date': result[i][1],'Link': 'exhibit_detail/'+result[i][2], 'Log Visit':'log_show/'+result[i][0]+'/'+str(result[i][1])} for i in range(len(result))]

    return render_template('visitor/search_show.html', form=form, items=items, title='Search Show')


@bp.route('/log_show/<string:name>/<string:date>', methods=['GET', 'POST'])
@login_required("VISITOR")
def log_show(name, date):

    sql = f"SELECT * FROM VISIT_SHOW WHERE " \
          f"(VISITOR = '{current_user.username}') AND " \
          f"(DATE_TIME = '{date}')"

    if db.query(sql).fetchone():
        flash(f"You have another show at the same time", 'warning')
        return redirect(url_for('visitor.search_show'))

    if dt.now() >= dt.strptime(date, '%Y-%m-%d %H:%M:%S'):
        sql = f"SELECT EXHIBIT FROM `SHOW` WHERE NAME = '{name}'"
        result = db.query(sql).fetchone()
        sql = f"INSERT INTO VISIT_SHOW (SHOW_NAME, DATE_TIME, VISITOR) VALUES ('{name}', '{date}', '{current_user.username}')"
        r = db.query(sql)
        sql = f"INSERT INTO VISIT_EXHIBIT (EXHIBIT, DATE_TIME, VISITOR) VALUES('{result[0]}', '{date}', '{current_user.username}')"
        s = db.query(sql)
    else:
        flash('Show not happened yet', 'warning')
        return redirect(url_for('visitor.search_show'))

    if not isinstance(r, pymysql.cursors.Cursor):
        flash('Impossible to log you in', 'warning')
        return redirect(url_for('visitor.search_show'))

    if not isinstance(s, pymysql.cursors.Cursor):
        flash('Impossible to log you in the exhibit', 'warning')
        return redirect(url_for('visitor.search_show'))

    flash("You successfully logged the visit", 'success')

    return redirect(url_for('visitor.search_show'))


@bp.route('/view_show_history', methods=['GET', 'POST'])
@login_required("VISITOR")
def view_show_history():
    form = ViewShowHistoryForm.new()

    username = current_user.username
    sort_by = form.sort_by.data if form.sort_by.data != "None" else "True"
    direction = "ASC" if form.direction.data is False else "DESC"
    sql = f"SELECT A.SHOW_NAME, A.DATE_TIME, B.EXHIBIT FROM " \
          f"(SELECT SHOW_NAME, DATE_TIME FROM VISIT_SHOW WHERE VISITOR= '{username}') AS A " \
          f"LEFT JOIN " \
          f"(SELECT NAME, DATE_TIME, EXHIBIT FROM `SHOW`) AS B " \
          f"ON (A.SHOW_NAME= B.NAME AND A.DATE_TIME= B.DATE_TIME) WHERE" \
          f"(SHOW_NAME = '{form.name.data}' or '{form.name.data}' = '') AND " \
          f"(A.DATE_TIME =  '{form.date.data}' or '{form.date.data}' = 'None') ORDER BY {sort_by} {direction}"
    result = db.query(sql).fetchall()
    items = [{'Name': result[i][0], 'Time': result[i][1], 'Exhibit': result[i][2]} for i in range(len(result))]

    return render_template('visitor/view_show_history.html', form=form, items=items, title='View Show History')


@bp.route('/search_animal', methods=['GET', 'POST'])
@login_required("VISITOR")
def search_animal():
    form = SearchAnimalForm.new()

    min_age = form.min_age.data
    max_age = form.max_age.data

    if min_age and min_age < 0:
        flash("Min must be positive", 'warning')
        return redirect(url_for("visitor.search_animal"))

    if max_age and max_age < 0:
        flash("Max must be positive", 'warning')
        return redirect(url_for("visitor.search_animal"))

    if (min_age and max_age) and max_age < min_age:
        flash("Max must be more than Min", 'warning')
        return redirect(url_for("visitor.search_animal"))

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
              'Type': result[i][4], 'Link': 'exhibit_detail/'+result[i][2]} for i in range(len(result))]

    return render_template('visitor/search_animal.html', form=form, items=items, title='Search Animal')


@bp.route('/exhibit_detail/<string:name>', methods=['GET', 'POST'])
@login_required("VISITOR")
def exhibit_detail(name):
    form = ExhibitDetail()

    sql = f"SELECT A.NAME, A.SIZE, A.WATER, B.C FROM " \
          f"(SELECT NAME, SIZE, WATER FROM EXHIBIT WHERE NAME = '{name}') AS A " \
          f"LEFT JOIN " \
          f"(SELECT EXHIBIT, COUNT(*) AS C FROM ANIMAL GROUP BY EXHIBIT) AS B " \
          f"ON (A.NAME=B.EXHIBIT)"

    result = db.query(sql).fetchall()
    items1 = [{'Name': result[i][0], 'Size': result[i][1], 'Water': result[i][2], 'Number of Animals': result[i][3]} for i in
             range(len(result))]

    sql = f"SELECT NAME, SPECIES FROM ANIMAL WHERE EXHIBIT = '{name}'"

    result = db.query(sql).fetchall()
    items2 = [{'Name': result[i][0], 'Species': result[i][1], 'Link':'/visitor/animal_detail/'+result[i][0]+'/'+result[i][1]} for i in range(len(result))]

    if form.validate_on_submit():
        sql = f"INSERT INTO VISIT_EXHIBIT (EXHIBIT, DATE_TIME, VISITOR) " \
              f"VALUES('{name}', '{dt.now()}', '{current_user.username}')"

        r = db.query(sql)

        if not isinstance(r, pymysql.cursors.Cursor):
            flash('Impossible to log visit', 'warning')
            return redirect(url_for('visitor.exhibit_detail', name=name))
        else:
            flash("You successfully logged the visit", 'success')
            return redirect(url_for('visitor.exhibit_detail', name=name))

    return render_template('visitor/exhibit_detail.html', form=form, items1=items1, items2=items2, title='Exhibit Details')


@bp.route('/animal_detail/<string:name>/<string:species>', methods=['GET', 'POST'])
@login_required("VISITOR")
def animal_detail(name, species):
    sql = f"SELECT NAME, SPECIES, EXHIBIT, AGE, TYPE FROM ANIMAL WHERE " \
          f"(NAME = '{name}') AND (SPECIES = '{species}')"

    result = db.query(sql).fetchall()
    items = [{'Name': result[i][0], 'Species': result[i][1], 'Exhibit': result[i][2], 'Age': result[i][3],
              'Type': result[i][4]} for i in range(len(result))]

    return render_template('visitor/animal_detail.html', items=items, title='Animal Details')
