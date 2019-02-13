from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.fields.html5 import IntegerField

from wtforms.validators import DataRequired, length

from ..utils.utils import get_animal_type_choices, get_exhibit_choices


class SearchAnimalForm(FlaskForm):
    name = StringField('Name')
    species = StringField('Species')
    min_age = IntegerField('Minimum Age')
    max_age = IntegerField('Maximum Age')
    exhibit = SelectField('Exhibit', choices=get_exhibit_choices())
    type = SelectField('Type', choices=get_animal_type_choices())
    search = SubmitField('Search')

    sort_by = SelectField('Order By', choices=[('True', ''), ('NAME', 'Name'),
                                              ('SPECIES', 'Species'), ('EXHIBIT', 'Exhibit'),
                                              ('AGE', 'Age'), ('TYPE', 'Type')])

    direction = BooleanField('Descending')

    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()

        # Update the choices for the agency field
        form.exhibit.choices = get_exhibit_choices()
        form.type.choices = get_animal_type_choices()
        return form


class AnimalCareForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    text = TextAreaField('Note', validators=[DataRequired(), length(max=200)], render_kw={"rows": 11, "cols": 50})
    submit = SubmitField('Log Note')
