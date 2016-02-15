from wtforms.fields import IntegerField, StringField, RadioField, SelectField
from wtforms import validators as wtfv
from wtforms_tornado import Form

"""Handles form validation for all pages."""

required_field_msg = 'This field is required.'


class LoginForm(Form):
    email = StringField(u'email', [wtfv.Email(message="Your email address was invalid"),
                                          wtfv.required(message="Please include an email address"),
                                          wtfv.Length(min=7, max=64, message="Email address must be 7-64 characters")])
    password = StringField(u'password',
                                  [wtfv.required("Please enter a password"),
                                   wtfv.Length(min=6, max=128, message="Password must be 6-128 characters")])


class RegistrationForm(Form):
    username = StringField(u'username',
                                  [wtfv.required(message="Please enter a username"),
                                   wtfv.Length(min=3, max=25, message="Username must be 3-25 characters")])
    email = StringField(u'email', [wtfv.Email(message="Not a valid email address"),
                                          wtfv.required(message="Please enter an email address"),
                                          wtfv.Length(min=7, max=64, message="Email address must be 7-64 characters")])

    school = StringField(u'school', [wtfv.required(message="Please enter a school"),
                                            wtfv.Length(min=3, max=15, message="school should be 3-15 characters")])
    password = StringField(u'password',
                                  [wtfv.required(message="Please enter a password"),
                                   wtfv.Length(min=6, max=128, message="Password must be 6-128 characters"),
                                   wtfv.EqualTo('password_confirm', message="Passwords did not match")])
    password_confirm = StringField(u'password_confirm',
                                          [wtfv.required(message="Please confirm your password"),
                                           wtfv.Length(min=6, max=128, message="Password must be 6-128 characters")])

class RateForm(Form):
    """Validates form data retrieved from the rating page."""
    name = StringField(u'name',
                       [wtfv.required(message=required_field_msg),
                        wtfv.length(min=5, max=30)])

    section = StringField(u'section',
                          [wtfv.required(message=required_field_msg),
                           wtfv.length(min=1, max=4)])

    semester = RadioField(u'semester',
                          [wtfv.required(message=required_field_msg)],
                          choices=[('fall', 'fall'),
                                   ('spring', 'spring'),
                                   ('summer', 'summer')])

    rating = IntegerField(u'rating',
                          [wtfv.required(message=required_field_msg),
                           wtfv.NumberRange(min=0, max=5)])
