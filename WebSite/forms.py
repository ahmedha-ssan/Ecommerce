from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , BooleanField,PasswordField, EmailField, IntegerField, FloatField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired , NumberRange, Length
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired()])
    username = StringField('UserName',validators=[DataRequired(),Length(min=2)])
    password1 = PasswordField('Enter your password',validators=[DataRequired(),Length(min=6)])
    password2 = PasswordField('Confirm your password',validators=[DataRequired(),Length(min=6)])
    submit = SubmitField('Sign Up')

class Loginform(FlaskForm):
    email = EmailField("Email",validators=[DataRequired()])
    password = PasswordField("Enter your password",validators=[DataRequired()])
    submit = SubmitField("Login")

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(),Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(),Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(),Length(min=6)])
    change_password = SubmitField('Change Password')

class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[FileRequired()])
    flash_sale = BooleanField('Flash Sale')
    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')

class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'),
                                                        ('Out for delivery', 'Out for delivery'),
                                                        ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])

    update = SubmitField('Update Status')