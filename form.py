from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional

class CVAform(FlaskForm):
    companyname = StringField('Company', validators = [DataRequired()])
    maturity = DateField('Date', format = '%Y-%m-%d', validators = [DataRequired()])
    facevalue = StringField('Credit', validators = [DataRequired()])
    adjvalue = StringField('Value', validators =[Optional()])
    submit = SubmitField('Evaluate')