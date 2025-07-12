from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired

class ItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=['Tops', 'Bottoms', 'Outerwear', 'Accessories'])
    size = StringField('Size')
    condition = SelectField('Condition', choices=['New', 'Good', 'Fair'])
    tags = StringField('Tags')
    image = FileField('Upload Image')
    submit = SubmitField('Submit')
