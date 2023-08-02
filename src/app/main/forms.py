from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo


class GCPCreateLogEntry(FlaskForm):
    levels = ('INFO', 'WARNING', 'ERROR')
    log_level = SelectField(label='Severity',  choices=levels)
    log_msg = StringField('Msg', validators=[DataRequired()])
    submit = SubmitField('Create entry log')


