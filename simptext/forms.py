# -*- coding: utf-8 -*-
"""
  The Login form
  The Entry Form
  The setting Form
  TODO: the registration form

@author wenlong
"""
from flask_wtf import Form
from wtforms import TextField, IntegerField, SubmitField, RadioField, SelectField, SelectMultipleField, widgets, validators, ValidationError

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(Form):
    username=TextField('username', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')


# The function is replaced by database
class EntryForm(Form):
    text=TextField('input', [validators.Length(min=4, max=25)])
    #words=StringField('password', [validators.Length(min=4, max=25)])
    #password= PasswordField('password',[validators.DataRequired()])
    submit = SubmitField('Submit')


# The function is used in setting
class SelectForm(Form):
    #wordinput = TextField("wordinput")
    wordinput = TextField("wordinput")
    wordlevel = SelectField('The level:', choices = [(0, 'level 0'), (1, 'level 1'), (2, 'level 2'), (3, 'level 3'), (4, 'level 4')], default=4)
    algs = MultiCheckboxField('The simplification procedures:', 
                                 choices = [ (1,'Punctuation (e.g. "I ate fish; he drank wine.")'), 
                                             (2, 'Coordination (e.g. "Peter ate fish and drank wine.")'),
                                             (3,'Subordinated Clauses (e.g. "Before he came, I left.")'),
                                             (4,'Adverbial Clauses (e.g. "Needing money, I begged my parents.")'), 
                                             (5,'Participial phrases (e.g. "Alicia, running down the street, tripped.")'),
                                             (6,'Adjectival Clauses (e.g. "The apple, which Peter ate, was red.")'),
                                             (7,'Appositive phrases (e.g. "Peter, my son, ate an apple.")'), 
                                             (8,'Passive voice (e.g. "Peter was hit by a bus.")' ),
                                             (9,'Parataxis (e.g. "Peter - nobody guessed it - showed up..")')], default=[1,2,3,4,5,6,7,8,9])
    submit =SubmitField("Submit")
