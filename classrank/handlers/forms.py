from wtforms.fields import IntegerField, StringField, RadioField, SelectField
from wtforms import validators as wtfv
from wtforms_tornado import Form

"""Handles form validation for all pages."""

required_field_msg = 'This field is required.'


class LoginForm(Form):
    """Validates form data retrieved from the login page."""
    email = StringField(u'email',
                        [wtfv.Email(),
                         wtfv.required(message=required_field_msg),
                         wtfv.Length(min=7, max=40)])

    password = StringField(u'password',
                           [wtfv.required(message=required_field_msg),
                            wtfv.Length(min=6, max=128)])


class RegistrationForm(Form):
    """Validates form data retrieved from the registration page."""
    username = StringField(u'username',
                           [wtfv.required(message=required_field_msg),
                            wtfv.Length(min=3, max=25)])

    email = StringField(u'email',
                        [wtfv.Email(),
                         wtfv.required(message=required_field_msg),
                         wtfv.Length(min=7, max=40)])

    # TODO: pull from the database's list of schools
    school = StringField(u'school',
                         [wtfv.required(message=required_field_msg),
                          wtfv.Length(min=3, max=15)])

    password = StringField(u'password',
                           [wtfv.required(message=required_field_msg),
                            wtfv.Length(min=6, max=128),
                            wtfv.EqualTo('password_confirm')])

    password_confirm = StringField(u'password_confirm',
                                   [wtfv.required(message=required_field_msg),
                                    wtfv.Length(min=6, max=128)])


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
