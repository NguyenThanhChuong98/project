from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from shop.models import Users

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    address = StringField('Address',
                          validators=[DataRequired(), Length(min=10, max=50)])
    date_of_birth = StringField('Date Of Birth',
                                validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That user name is already taken.Please choose another one')

    def validate_email(self, email):
        email = Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already taken.Please choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    address = StringField('Address',
                          validators=[DataRequired(), Length(min=10, max=50)])
    date_of_birth = StringField('Date Of Birth',
                                validators=[DataRequired()])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That user name is already taken.Please choose another one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already taken.Please choose another one')

class ProductForm(FlaskForm):
    productname = StringField('Product Name',validators=[DataRequired(),Length(min=2, max=20)])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    price = IntegerField('Price',validators=[DataRequired()])
    product_description = TextAreaField('Product Description',validators=[DataRequired(),Length(min=2, max=500)])
    image_product = FileField('Product Picture',validators=[FileAllowed(['jpg','png']),FileRequired()])
    submit = SubmitField('Create')

class CategoryForm(FlaskForm):
    categoryname = StringField('Category Name',validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Create')
