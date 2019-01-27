from flask import Flask, render_template, url_for, flash, redirect, request
from flask_bcrypt import Bcrypt
##from flask_login import login_user, current_user, logout_user, login_required,login_manager
import pyodbc, string
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


global is_login, email 
is_login = False
email = ""


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


def special_char(str):
    for char in str:
        if char in string.punctuation:
            return True
    return False


def findFileName(str):
    s = ""
    ok = False
    for i in str:
        if i == '\'':
            if ok:
                break
            ok = True
            continue
        if ok:
            s += i
    return s

def insertBook(title, theBook):
    books = db.execute(''' select * from book ''').fetchall()
    db.commit()
    for item in books:
        if item.title == title:
            return
    theBook = str(theBook)
    theBook = findFileName(theBook)
    db.execute(f'''INSERT INTO book (title, TheBook) VALUES ('{title}', '{theBook}');''')
    db.commit()


def deletebook(title):
    db.execute(f''' execute deleteBook '{title}' ''')
    db.commit()

def insertAuthor(author):
    authors = db.execute(''' select * from author ''').fetchall()
    db.commit()
    for item in authors:
        if item.author_name == author:
            return
    db.execute(f''' insert into author (author_name) values ('{author}'); ''')
    db.commit()

def deleteAuthor(author_name):
    db.execute(f''' execute deleteAuthor '{author_name}' ''')
    db.commit()

def insertIntoAuthorBook(authorName, title):
    book = db.execute(f''' execute getBookAuthor '{title}', '{authorName}' ''').fetchone()
    db.commit()
    if book != None:
        return
    db.execute(f''' execute insertIntoAuthor_Book '{title}', '{authorName}' ''')
    db.commit()

def insertAuthorGroup(author_name, type):
    author = db.execute(f''' execute getAuthor_Group '{author_name}', '{type}' ''').fetchone()
    db.commit()
    if author != None:
        return
    db.execute(f''' execute insertIntoAuthor_Group '{author_name}', '{type}' ''')
    db.commit()

def insertIntoBookLang(title, lang):
    book = db.execute(f''' execute getBookOfLang '{title}', '{lang}' ''').fetchone()
    db.commit()
    if book != None:
        return
    db.execute(f''' execute insertIntoBook_Lang '{title}', '{lang.lower()}' ''')
    db.commit()
   
def insertIntoBookGroup(title, group):
    book = db.execute(f''' execute getBookOfType '{title}', '{group}' ''').fetchone()
    db.commit()
    if book != None:
        return
    db.execute(f''' execute insertIntoBook_Group '{title}', '{group.lower()}' ''')
    db.commit()

def delete_user(mail):
    db.execute(f''' execute deleteuser '{mail}' ''')
    db.commit()

def Bookmark(isbn):
    global email
    # making sure that bookmark doesn't exist 
    bookmark = db.execute(f''' execute getSpacifBookmark '{email}', {isbn} ''').fetchone()
    db.commit()
    if bookmark != None:
        return
    db.execute(f''' insertFavBook '{email}', {isbn} ''')
    db.commit()

def RemoveBookmark(isbn):
    global email
    db.execute(f''' RemoveBookmark '{email}', {isbn} ''')
    db.commit()


def updateUserProfile(form):
    global email
    first = form.first.data
    last = form.last.data
    bio = form.bio.data
    pic = str(form.picture.data)
    pic = findFileName(pic)
    db.execute(f''' execute updateUserProfile '{email}', '{first}', '{last}', '{pic}', '{bio}' ''')
    db.commit()

    
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                    "Server=DELL;"
                    "Database=Library;"
                    "Trusted_Connection=yes;")


bcrypt = Bcrypt()


@app.route("/")
@app.route("/home")
def home():
    global is_login, email
    if is_login:
        if email == 'admin@blog.com':
            return render_template('home.html', st="yes", admin = 'admin')
        return render_template('home.html', st="yes")
    return render_template('home.html')


@app.route("/about")
def about():
    global is_login, email
    if is_login:
        if email == 'admin@blog.com':
            return render_template('about.html', title='About', st = "yes", admin = 'admin')
        return render_template('about.html', title='About', st = "yes")
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    global is_login, email
    if is_login:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        if '\'' in email:
            flash('Check the entered e-mail', 'danger')
            return render_template('register.html', title = 'Register', form = form)
        DBEmail = db.execute(f''' SELECT * FROM [user] WHERE email LIKE '{email}'; ''').fetchone()
        if DBEmail != None:
            flash('E-mail already exists!', 'danger')
            return render_template('register.html', title = 'Register', form = form)
        password = form.password.data
        confirm_password = form.confirm_password.data
        if special_char(password):
            flash('''Password shouldn't contain special characters such as''' + string.punctuation, 'danger')
            return render_template('register.html', title = 'Register', form = form)
        if password != confirm_password:
            flash('Check you password', 'danger')
            return render_template('register.html', title = 'Register', form = form)
        password = bcrypt.generate_password_hash(password).decode("utf-8")
        first = form.first_name.data
        last = form.last_name.data
        db.execute(f''' INSERT INTO [user] (email, password, firstName, lastName) VALUES ('{email}', '{password}', '{first}', '{last}'); ''')
        db.commit()
        flash(f'Account created for {form.first_name.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    global is_login, email
    if is_login:
        return redirect(url_for("home"))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        if '\'' in email:
            flash('Check the entered e-mail', 'danger')
            return render_template('login.html', title = 'login', form = form)
        password = form.password.data
        if special_char(password):
            flash('''Password shouldn't contain special characters such as ''' + string.punctuation, 'danger')
            return render_template('login.html', title = 'login', form = form)
        
        user = db.execute(f''' SELECT * FROM [user] WHERE email LIKE '{email}' ; ''').fetchone()
        if user == None or bcrypt.check_password_hash(user.password, password) == False:
            flash('Check your email and password', 'danger')
            return render_template('login.html', title = 'Login', form = form)
        is_login = True
        if email == 'admin@blog.com':
            render_template("home.html", st = "yes", admin = 'admin')
            flash('Welcome Sir', 'success')
            return render_template("home.html", st = "yes", admin = 'admin')
        else:
            render_template("home.html", st = "yes", form = form)
            flash('Welcome '+ user.firstName, 'success')
            return render_template("home.html", st = "yes")
    return render_template('login.html', title='Login', form=form)


@app.route("/account<string:edit>", methods=['GET', 'POST'])
@app.route("/account", methods=['GET', 'POST'])
def account(edit = ""):
    global email, is_login
    if not is_login:
       return redirect(url_for("home"))
    user = db.execute(f''' select * from [user] where email like '{email}' ''').fetchone()
    db.commit()
    if user.profilePicture == None:
        current_user_image_file= "defaultPic.png"
    else:
        current_user_image_file= user.profilePicture
    image_file = url_for('static', filename= current_user_image_file)
    if edit != "":
        form = AccountForm()
        if form.validate_on_submit() and is_login:
            updateUserProfile(form)
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        if email == 'admin@blog.com':
            return render_template('account.html', title='Account', image_file=image_file, form=form, st = "yes", edit = True, admin = "admin", user = user)
        return render_template('account.html', title='Account', image_file=image_file, form=form, st = "yes", edit = True, user = user)
    else:
        if email == 'admin@blog.com':
            return render_template('account.html', title='Account', image_file=image_file, st = "yes", admin = "admin", edit = False, user = user)
        return render_template('account.html', title='Account', image_file=image_file, st = "yes", edit = False, user = user)

@app.route("/addpage", methods = ['POST', 'GET'])
def addpage():
    global is_login
    if is_login and email == 'admin@blog.com':
        form = AddForm()
        if form.validate_on_submit():
            file = form.book.data
            author_name = form.authorName.data
            type = form.authorType.data
            insertBook(form.title.data, file)
            insertAuthor(author_name)
            insertAuthorGroup(author_name, type)
            insertIntoAuthorBook(author_name, form.title.data)
            insertIntoBookLang(form.title.data, form.language.data)
            insertIntoBookGroup(form.title.data, form.type.data)
        return render_template("addpage.html", form = form, st = "yes", admin = 'admin')
    return redirect(url_for("home"))
   

@app.route("/delete", methods = ['POST', 'GET'])
def delete():
    global is_login, email
    if is_login and email == 'admin@blog.com':
        form = Delete()
        if form.validate_on_submit():
            title = form.name_book.data
            author = form.author_name.data
            deletebook(title)
            deleteAuthor(author)
            flash(title + ' Delteted', 'success')
        return render_template('delete.html', title = 'delete', st = "yes", form = form, admin = 'admin')
    return redirect(url_for("home"))


@app.route("/book/<int:ISBN>", methods = ['POST', 'GET'])
@app.route("/book/<string:lang>", methods = ['POST', 'GET'])
def book(ISBN = 0, lang = ""):
    global is_login, email
    form = BookSearch()
    title = form.title.data    
    language = form.lang.data
    type = form.type.data
    print(type, language)
    if title != None and title != '':
        book = db.execute(f''' select * from book where title like '%{title}%' ''').fetchall()
    elif language != None and language != '':
        book = db.execute(f''' select * from booksOfLang('{language}') ''').fetchall()
    elif type != None and type != '':
        book = db.execute(f''' select * from bookOfType('{type}') ''').fetchall()
    elif lang != "" and lang[0] != 'T' and lang[0] != '0':
        book = db.execute(f''' select * from booksOfLang('{lang}') ''').fetchall()
    elif lang != "" and lang[0] == 'T':
        lang = lang[1:]
        book = db.execute(f''' select * from bookOfType('{lang}') ''').fetchall()
    elif lang != "" and lang[0] == '0':
        lang = lang[1:]
        book = db.execute(f''' select * from getBooksOF('{lang}') ''').fetchall()
    else:
        book = db.execute(''' select * from book ''').fetchall()
    db.commit()
    if ISBN != 0 and is_login:
        Bookmark(ISBN)
    if is_login:
        if email == "admin@blog.com":
           return render_template("book.html", book = book, title = "Book", admin = 'admin', st = 'yes', checked = "", form = form)
        return render_template("book.html", book = book, title = "Book", st = 'yes', checked = "", form = form)
    return render_template("book.html", book = book, title = "Book", checked = "", form = form)

@app.route("/admin have the power/<string:mail>", methods = ['POST', 'GET'])
@app.route("/admin have the power", methods = ['POST', 'GET'])
def admin_have_the_power(mail=''):
    users = db.execute('''select * from [user]''').fetchall()
    db.commit()
    global email 
    global is_login
    if is_login:
       if email == "admin@blog.com":
           if mail!='':
               delete_user(mail)
           return render_template("admin have the power.html", users = users, title = "delete users", admin = 'admin', st = 'yes')



@app.route('/favBook/<int:isbn>')
def favBook(isbn = 0):
    global email, is_login
    if not is_login:
       return redirect(url_for("home"))
    form = FavBook()
    if isbn != 0:
        RemoveBookmark(isbn)
    book = db.execute(f''' execute getFavBook '{email}' ''').fetchall()
    db.commit()
    if email == "admin@blog.com":
        return render_template("favbook.html", book = book, title = "Book", admin = 'admin', st = 'yes', form = form)
    return render_template("favbook.html", book = book, title = "Book", st = 'yes', form = form)


@app.route("/author", methods=['POST', 'GET'])
def author():
    global is_login, email
    form = AuthorSearch()
    name = form.name.data
    type = form.type.data
    if name != None and name != "":
        author = db.execute(f''' select * from author where author_name like '%{name}%' ''').fetchall()
    elif type != None and type != "":
        author = db.execute(f''' select * from authorOfType('{type}') ''').fetchall()
    else:
        author = db.execute(''' select * from author ''').fetchall()
    db.commit()
    if is_login:
        if email == "admin@blog.com":
           return render_template("author.html", author = author, title = "author", admin = 'admin', st = 'yes', form = form)
        return render_template("author.html", author = author, title = "author", st = 'yes', form = form)
    return render_template("author.html", author = author, title = "author", form = form)


@app.route("/logout")
def logout():
    global is_login, email
    is_login = False
    email = ""
    render_template("layout.html", st = "no")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
