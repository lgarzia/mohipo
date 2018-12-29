from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    role = StringField('What is your role?', validators=[Required()])
    language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Submit')