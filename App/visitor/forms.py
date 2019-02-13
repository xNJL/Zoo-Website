from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateField, IntegerField

from ..utils.utils import get_animal_type_choices, get_exhibit_choices


class SearchExhibitForm(FlaskForm):
    name = StringField('Name')

    # still need to set constraint that min < max
    min_animal = IntegerField('Min Number of Animals')
    max_animal = IntegerField('Max Number of Animals')

    min_size = IntegerField('Minimum Size')
    max_size = IntegerField('Maximum Size')

    water = SelectField('Water', choices=[('', ''), (1, 'yes'), (0, 'no')])
    sort_by = SelectField('Order By', choices=[('True', ''), ('NAME', 'Name'),
                                              ('WATER', 'Water'), ('SIZE', 'Size'),
                                              ('C', 'Number of Animals')])

    direction = BooleanField('Descending')

    search = SubmitField('Search')


class SearchAnimalForm(FlaskForm):
    name = StringField('Name')
    species = StringField('Species')

    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())

    # still need to set constraint that min < max
    min_age = IntegerField('Minimum Age')
    max_age = IntegerField('Maximum Age')

    type = SelectField('Type', choices=get_animal_type_choices())
    sort_by = SelectField('Order By', choices=[('True', ''), ('NAME', 'Name'),
                                              ('SPECIES', 'Species'), ('EXHIBIT', 'Exhibit'),
                                              ('AGE', 'Age'), ('TYPE', 'Type')])

    direction = BooleanField('Descending')

    search = SubmitField('Search')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.exhibit.choices = get_exhibit_choices()
        form.type.choices = get_animal_type_choices()
        return form


class SearchShowForm(FlaskForm):
    name = StringField('Name')
    date = DateField('Date')

    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())

    sort_by = SelectField('Order By', choices=[('True', ''), ('NAME', 'Name'),
                                              ('EXHIBIT', 'Exhibit'), ('DATE_TIME', 'Date')])
    direction = BooleanField('Descending')

    search = SubmitField('Search')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.exhibit.choices = get_exhibit_choices()
        return form


class ViewExhibitHistoryForm(FlaskForm):
    name = StringField('Name')

    # still need to set constraint that min < max
    min_visits = IntegerField('Min Number of Visits')
    max_visits = IntegerField('Max Number of Visits')

    date = DateField('Date')
    sort_by = SelectField('Order By', choices=[('True', ''), ('NAME', 'Name'),
                                              ('WATER', 'Water'), ('SIZE', 'Size'),
                                              ('C', 'Number of Animals')])

    direction = BooleanField('Descending')

    search = SubmitField('Search')


class ViewShowHistoryForm(FlaskForm):
    name = StringField('Name')

    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())
    date = DateField('Date')

    sort_by = SelectField('Order By', choices=[('True', ''), ('NAME', 'Name'),
                                              ('EXHIBIT', 'Exhibit'), ('DATE_TIME', 'Date')])
    direction = BooleanField('Descending')

    search = SubmitField('Search')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.exhibit.choices = get_exhibit_choices()
        return form


class ExhibitDetail(FlaskForm):
    search = SubmitField('Log visit')