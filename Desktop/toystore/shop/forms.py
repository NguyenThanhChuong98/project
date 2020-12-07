from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from shop.models import Users

class RegistrationForm(FlaskForm):
    username = StringField('User Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    address = StringField('Address',
                          validators=[DataRequired(), Length(min=10, max=50)])
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d')
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
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d')
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
    product_name = StringField('Product Name',validators=[DataRequired(),Length(min=2, max=20)])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    price = IntegerField('Price',validators=[DataRequired()])
    age_recommendation = StringField('Age Recommendation',validators=[DataRequired()])
    dimensions = StringField('Dimensions',validators=[DataRequired(),Length(min=2, max=500)])
    country_of_design = StringField('Country Of Design',validators=[DataRequired(),Length(min=2, max=500)])
    country_of_manufacture = StringField('Country Of Manufacture',validators=[DataRequired(),Length(min=2, max=500)])
    primary_material = StringField('Primary Material',validators=[DataRequired(),Length(min=2, max=500)])
    assembly_required = StringField('Assembly Required',validators=[DataRequired(),Length(min=2, max=500)])
    gift_wrap = StringField('Gif Wrap',validators=[DataRequired(),Length(min=2, max=500)])
    image_product = FileField('Image Product', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('Create')

class CategoryForm(FlaskForm):
    category_name = StringField('Category Name',validators=[DataRequired(),Length(min=2,max=20)])
    submit = SubmitField('Create')

class ShipperForm(FlaskForm):
    shipper_name = StringField('Shipper Name', validators=[DataRequired(),Length(min=2, max=20)])
    date_of_birth = DateField('Date Of Birth', format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Create')