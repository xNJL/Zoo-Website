from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.fields.html5 import DateField, TimeField, IntegerField
from wtforms.validators import DataRequired

from ..utils.utils import get_animal_type_choices, get_exhibit_choices, get_staff_choices


class ViewShowForm(FlaskForm):
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


class ViewAnimalForm(FlaskForm):
    name = StringField('Name')
    species = StringField('Species')

    # still need to set constraint that min < max
    min_age = IntegerField('Minimum Age')
    max_age = IntegerField('Maximum Age')

    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())

    type = SelectField('Type', choices=[('', ''), ('Mammal', 'Mammal'), ('Bird', 'Bird'), ('Amphibian', 'Amphibian'),
                                        ('Reptile', 'Reptile'),
                                        ('Fish', 'Fish'), ('Invertebrate', 'Invertebrate')])
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
        return form


class AddShowForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())
    staff = SelectField('Staff', choices=get_staff_choices())

    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])

    submit = SubmitField('Add Show')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.exhibit.choices = get_exhibit_choices()
        form.staff.choices = get_staff_choices()
        return form


class AddAnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])

    type = SelectField('Type', choices=[('', ''), ('Mammal', 'Mammal'), ('Bird', 'Bird'), ('Amphibian', 'Amphibian'),
                                        ('Reptile', 'Reptile'),
                                        ('Fish', 'Fish'), ('Invertebrate', 'Invertebrate')])
    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())

    submit = SubmitField('Add Animal')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.exhibit.choices = get_exhibit_choices()
        return form


class SearchUser(FlaskForm):
    username = StringField('Search by Username')
    email = StringField('Search by Email')
    search = SubmitField('Search')
    sort_by = SelectField('Order By', choices=[('True', ''), ('USERNAME', 'Username'),
                                              ('EMAIL', 'Email')])
    direction = BooleanField('Descending')

    submit = SubmitField('Search')
