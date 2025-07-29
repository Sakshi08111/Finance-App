from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class IncomeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    source = StringField('Source', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Income')

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Expense')