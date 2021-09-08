from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired


class DataUpload(FlaskForm):
    dataset = FileField('Upload file', validators=[FileAllowed(['txt', 'csv', 'html','json','xlsx','sql']), DataRequired()])
    submit = SubmitField('Upload Dataset')
