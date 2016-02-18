from wtforms.fields import IntegerField, StringField, RadioField, SelectField
from wtforms import validators as wtfv
from wtforms.validators import ValidationError
from wtforms_tornado import Form

"""Handles form validation for all pages."""

password_min = 6
password_max = 128
email_min = 7
email_max = 64

required_field_msg = "This field is required."
password_length_msg = "Password must be %d-%d characters" % (password_min, password_max)
email_length_msg = "Email address must be %d-%d characters" % (email_min, email_max)


class LoginForm(Form):
    email = StringField(u'email', [wtfv.Email(message="Your email address was invalid"),
                                          wtfv.required(message="Please include an email address"),
                                          wtfv.Length(min=email_min, max=email_max, message=email_length_msg)])
    password = StringField(u'password',
                                  [wtfv.required("Please enter a password"),
                                   wtfv.Length(min=password_min, max=password_max, message=password_length_msg)])


class RegistrationForm(Form):
    username = StringField(u'username',
                                  [wtfv.required(message="Please enter a username"),
                                   wtfv.Length(min=3, max=25, message="Username must be 3-25 characters")])
    email = StringField(u'email', [wtfv.Email(message="Not a valid email address"),
                                          wtfv.required(message="Please enter an email address"),
                                          wtfv.Length(min=7, max=64, message=email_length_msg)])

    school = StringField(u'school', [wtfv.required(message="Please enter a school"),
                                            wtfv.Length(min=3, max=15, message="School must be 3-15 characters")])
    password = StringField(u'password',
                                  [wtfv.required(message="Please enter a password"),
                                   wtfv.Length(min=password_min, max=password_max, message=password_length_msg),
                                   wtfv.EqualTo('password_confirm', message="Passwords did not match")])
    password_confirm = StringField(u'password_confirm',
                                          [wtfv.required(message="Please confirm your password"),
                                           wtfv.Length(min=password_min, max=password_max, message=password_length_msg)])

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


def optionalLength(min, max, message):
  """Ensures a field is either empty, or between min-max characters"""
  def _optionalLength(form, field):
    if len(field.data) > 0:
      if len(field.data) < min or len(field.data) > max:
        raise ValidationError(message)

  return _optionalLength

class SettingsForm(Form):
  """Validates form data from the user's settings page."""
  current_password = StringField(u'current_password',
                          [wtfv.required(message=required_field_msg)])

  new_password = StringField(u'new_password',
                          [optionalLength(min=6, max=128, message=password_length_msg),
                           wtfv.EqualTo('new_password_confirm', message="Passwords did not match")])

  new_password_confirm = StringField(u'new_password_confirm',
                          [optionalLength(min=6, max=128, message=password_length_msg)])

  new_email = StringField(u'email', [wtfv.Email(message="Not a valid email address"),
                          wtfv.required(message=required_field_msg),
                          wtfv.Length(min=7, max=64, message=email_length_msg)])
