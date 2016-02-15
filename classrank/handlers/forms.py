from wtforms import fields
from wtforms import validators as wtfv
from wtforms_tornado import Form


class LoginForm(Form):
    email = fields.StringField(u'email', [wtfv.Email(message="Your email address was invalid"),
                                          wtfv.required(message="Please include an email address"),
                                          wtfv.Length(min=7, max=64, message="Email address must be 7-64 characters")])
    password = fields.StringField(u'password',
                                  [wtfv.required("Please enter a password"),
                                   wtfv.Length(min=6, max=128, message="Password must be 6-128 characters")])


class RegistrationForm(Form):
    username = fields.StringField(u'username',
                                  [wtfv.required(message="Please enter a username"),
                                   wtfv.Length(min=3, max=25, message="Username must be 3-25 characters")])
    email = fields.StringField(u'email', [wtfv.Email(message="Not a valid email address"),
                                          wtfv.required(message="Please enter an email address"),
                                          wtfv.Length(min=7, max=64, message="Email address must be 7-64 characters")])
    # TODO: pull from the database's list of schools
    school = fields.StringField(u'school', [wtfv.required(message="Please enter a school"),
                                            wtfv.Length(min=3, max=15, message="school should be 3-15 characters")])
    password = fields.StringField(u'password',
                                  [wtfv.required(message="Please enter a password"),
                                   wtfv.Length(min=6, max=128, message="Password must be 6-128 characters"),
                                   wtfv.EqualTo('password_confirm', message="Passwords did not match")])
    password_confirm = fields.StringField(u'password_confirm',
                                          [wtfv.required(message="Please confirm your password"),
                                           wtfv.Length(min=6, max=128, message="Password must be 6-128 characters")])
