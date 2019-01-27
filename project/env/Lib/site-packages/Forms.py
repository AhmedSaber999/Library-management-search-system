from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired(), Length(min=2, max=15, message = 'First Name should be at least 2 characters long and at most 15. Please try another.')])
    last_name = StringField('Last Name',  validators=[DataRequired(), Length(min=2, max=15, message = 'Last Name should be at least 2 characters long and at most 15. Please try another.')])
    email = StringField('Email',validators=[DataRequired(), Email(message = 'Enter the email address in the format "someone@example.com".')])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email(message = 'Invaild email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AddForm(FlaskForm):
    authorName = StringField('Author Name',validators=[DataRequired()])
    title = StringField('Title',validators=[DataRequired()])
    language = StringField('Language',validators=[DataRequired()])
    authorType = StringField('Category Of The Author',validators=[DataRequired()])
    type = StringField('Category Of The Book',validators=[DataRequired()])
    book = FileField('Upload The Book', validators=[DataRequired()])
    submit = SubmitField('Upload')

class Delete(FlaskForm):
    name_book = StringField('Delete Book')
    author_name = StringField('Delete Author')
    submit = SubmitField('Delete')


class AccountForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    bio = StringField('Biography')
    submit = SubmitField('Update')


class BookSearch(FlaskForm):
    title = StringField('Title')
    lang = StringField('Language')
    type = StringField('Category')
    submit = SubmitField('Search')
    bookmark = SubmitField('Bookmark')
    view = SubmitField('View')
    download = SubmitField('Download')

class AuthorSearch(FlaskForm):
    name = StringField('Author Name')
    type = StringField('Category')
    submit = SubmitField('Search')
    list = SubmitField('List Of His Books')

class FavBook(FlaskForm):
    remove = SubmitField('remove')
    view = SubmitField('View')
    download = SubmitField('Download')
