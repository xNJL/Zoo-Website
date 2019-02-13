from datetime import datetime as dt

from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from . import bp
from .forms import SearchAnimalForm, AnimalCareForm
from ..__init__ import db
from ..utils.utils import login_required


@bp.route('/')
@login_required("STAFF")
def staff():
    return render_template('staff/staff.html')


@bp.route('/search_animal',  methods=['GET', 'POST'])
@login_required("STAFF")
def search_animal():
    form = SearchAnimalForm.new()
    min_age = form.min_age.data
    max_age = form.max_age.data

    if min_age and min_age < 0:
        flash("Min must be positive", 'warning')
        return redirect(url_for("staff.search_animal"))

    if max_age and max_age < 0:
        flash("Max must be positive", 'warning')
        return redirect(url_for("staff.search_animal"))

    if (min_age and max_age) and max_age < min_age:
        flash("Max must be more than Min", 'warning')
        return redirect(url_for("staff.search_animal"))

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
              'Type': result[i][4], 'Link': 'search_animal/'+result[i][0]+'/'+result[i][1]} for i in range(len(result))]

    return render_template('staff/search_animal.html', form=form, items=items, title='Search Animal')



@bp.route('/view_shows')
@login_required("STAFF")
def view_shows():
    sql = f"SELECT NAME, DATE_TIME, EXHIBIT FROM `SHOW` WHERE HOST = '{current_user.username}'"

    result = db.query(sql).fetchall()

    items = [{'Name': result[i][0], 'Date': result[i][1], 'Exhibit': result[i][2]} for i in range(len(result))]

    return render_template('staff/view_shows.html', items=items, title='View Show')


@bp.route('/search_animal/<string:name>/<string:species>', methods=['GET', 'POST'])
@login_required("STAFF")
def animal_care(name, species):
    sql = f"SELECT NAME, SPECIES, EXHIBIT, AGE, TYPE FROM ANIMAL WHERE " \
          f"(NAME = '{name}') AND (SPECIES = '{species}')"

    result = db.query(sql).fetchall()
    items1 = [{'Name': result[i][0], 'Species': result[i][1], 'Exhibit': result[i][2], 'Age': result[i][3],
              'Type': result[i][4]} for i in range(len(result))]

    form = AnimalCareForm()

    if form.validate_on_submit():
        sql = f"INSERT INTO ANIMAL_CARE (ANIMAL, SPECIES, STAFF_MEMBER, DATE_TIME, NOTE)" \
              f"VALUES ('{name}', '{species}', '{current_user.username}', " \
              f"'{dt.now()}', '{form.text.data}')"

        db.query(sql)

        form.text.data = None

    sql = f"SELECT STAFF_MEMBER, NOTE, DATE_TIME FROM ANIMAL_CARE WHERE ANIMAL = '{name}'"

    result = db.query(sql).fetchall()
    items2 = [{'staff Member': result[i][0], 'Note': result[i][1], 'Time': result[i][2]} for i in range(len(result))]

    return render_template('staff/animal_care.html', items1=items1, items2=items2, form=form, title='Animal Care')
