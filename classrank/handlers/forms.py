from wtforms import fields
from wtforms import validators as wtfv
from wtforms_tornado import Form


class LoginForm(Form):
    email = fields.StringField(u'email', [wtfv.Email(), wtfv.required(),
                                          wtfv.Length(min=7, max=40)])
    password = fields.StringField(u'password',
                                  [wtfv.required(), wtfv.Length(min=6, max=128)])


class RegistrationForm(Form):
    username = fields.StringField(u'username',
                                  [wtfv.required(), wtfv.Length(min=3, max=25)])
    email = fields.StringField(u'email', [wtfv.Email(), wtfv.required(),
                                          wtfv.Length(min=7, max=40)])
    # TODO: pull from the database's list of schools
    school = fields.StringField(u'school', [wtfv.required(), wtfv.Length(min=3, max=15)])
    password = fields.StringField(u'password',
                                  [wtfv.required(), wtfv.Length(min=6, max=128),
                                   wtfv.EqualTo('password_confirm')])
    password_confirm = fields.StringField(u'password_confirm',
                                          [wtfv.required(), wtfv.Length(min=6, max=128)])

class AddCourse(Form):
    name = fields.StringField(u'name',
                              [wtfv.required(), wtfv.Length(min=3, max=128)])
    abbreviation = fields.StringField(u'name',
                                      [wtfv.required(), wtfv.Length(min=3, max=25)])
    description = fields.StringField(u'name', [wtfv.Length(min=0, max=128)])
    section = fields.StringField(u'name',
                                 [wtfv.required(), wtfv.Length(min=3, max=25)])
