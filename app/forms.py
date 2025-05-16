from wtforms import Form, BooleanField, StringField, validators

class ResetPsswrdRequestFrom(Form):
    email = StringField('Email', validators=[])