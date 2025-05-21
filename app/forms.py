from wtforms import Form, StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo 



class ResetPsswrdRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )   
    submit = SubmitField("Confirm Password Reset") 
