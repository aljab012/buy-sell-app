# main.py


from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import *
from wtforms import BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm

from . import db


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=3, max=35)])
    name = StringField('name', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    phone = StringField('Phone', validators=[validators.DataRequired()])
    confirm = PasswordField('Repeat Password')

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/quote')
@login_required
def qoute():
    return render_template('quote.html', name=current_user.name)

@main.route('/profile')
@login_required
def profile():
    books = db.session.execute('select * from book where book.seller_id == {}'.format(current_user.id)).fetchall()
    events = db.session.execute('select * from event where event.owner_id == {}'.format(current_user.id)).fetchall()
    return render_template('profile.html', user=current_user, books=books,events= events)

@main.route('/remove_book/<int:book_id>')
@login_required
def remove_book(book_id):
    print(book_id)
    db.session.execute('delete from book where book.id == {}'.format(book_id))
    db.session.commit()
    books = db.session.execute('select * from book where book.seller_id == {}'.format(current_user.id)).fetchall()
    events = db.session.execute('select * from event where event.owner_id == {}'.format(current_user.id)).fetchall()
    return render_template('profile.html', user=current_user, books=books,events= events)

@main.route('/remove_event/<int:event_id>')
@login_required
def remove_event(event_id):
    db.session.execute('delete from event where event.id == {}'.format(event_id))
    db.session.commit()
    books = db.session.execute('select * from book where book.seller_id == {}'.format(current_user.id)).fetchall()
    events = db.session.execute('select * from event where event.owner_id == {}'.format(current_user.id)).fetchall()
    return render_template('profile.html', user=current_user, books=books,events= events)

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('main.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

# @main.route('/signup')
# def signup():
#     return render_template('signup.html')

@main.route('/signup', methods=['POST','GET'])
def signup():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        name = form.name.data
        password = form.password.data
        phone = form.phone.data
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        check_phone = User.query.filter_by(telephone=phone).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again  
            flash('Email address already exists')
            return render_template('signup.html',form=form)
            
        if check_phone: # if a user is found, we want to redirect back to signup page so user can try again  
            flash('Phone already already exists')
            return render_template('signup.html',form=form)

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), telephone=phone )

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('signup.html', form=form)



@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.profile'))


@main.route('/sellBook')
@login_required
def sellBook():
    category = db.session.execute('select * from category').fetchall()
    return render_template('sellBook.html', category=category)

@main.route('/book')
@login_required
def book():
    books = db.session.execute('select * from book').fetchall()
    category = db.session.execute('select * from category').fetchall()
    users = db.session.execute('select * from user').fetchall()
    return render_template('book.html', books=books, category=category, users=users)

@main.route('/SelectBook')
@login_required
def SelectBook():
    subject = request.args['selected_major']
    if subject == "0":
        return redirect('/book')

    SelectedBook = db.session.execute(f'select * from book where category_id= {subject} order by title').fetchall()
    category = db.session.execute('select * from category').fetchall()
    users = db.session.execute('select * from user').fetchall()
    return render_template('book.html', books=SelectedBook, category=category, users=users)

@main.route('/sellBook', methods=['POST'])
@login_required
def book_post():

    title = request.form.get('title')
    details = request.form.get('details')
    price = request.form.get('price')
    pub_date = request.form.get('pub_date')
    category_id = request.form.get('category_id')

    if title == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter the name of the book')
        return redirect(url_for('main.book'))
    
    if details == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter the book\'s details')
        return redirect(url_for('main.book'))
    

    if price == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter a price for the book')
        return redirect(url_for('main.book'))

    if category_id == "0": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please select a category')
        return redirect(url_for('main.book'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_book = Book(title=title, details=details, price=price, pub_date=pub_date, category_id=category_id,seller=current_user)

    # add the new user to the database
    db.session.add(new_book)
    db.session.commit()

    flash('The book {} add successfully'.format(title))
    return redirect('/book')



@main.route('/event')
@login_required
def event():
    events = db.session.execute('select * from event').fetchall()
    category = db.session.execute('select * from category').fetchall()
    users = db.session.execute('select * from user').fetchall()

    return render_template('event.html', events=events, category=category, users=users)


@main.route('/SelectEvent')
@login_required
def SelectEvent():
    subject = request.args['selected_event']
    if subject == "0":
        return redirect('/event')

    Selectedgroup = db.session.execute(f'select * from event where category_id= {subject} order by event_name').fetchall()
    category = db.session.execute('select * from category').fetchall()
    users = db.session.execute('select * from user').fetchall()

    return render_template('event.html', events=Selectedgroup, category=category, users=users)


@main.route('/event', methods=['POST'])
@login_required
def event_post():

    title = request.form.get('title')
    details = request.form.get('details')
    time = request.form.get('time')
    place = request.form.get('place')
    category_id = request.form.get('category_id')

    if title == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter the name of the event')
        return redirect(url_for('main.event'))
    
    if details == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter the event\'s details')
        return redirect(url_for('main.event'))
    

    if time == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter a time for the event')
        return redirect(url_for('main.event'))

    if place == "": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please enter a place for the event')
        return redirect(url_for('main.event'))

    if category_id == "0": # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Please select a category')
        return redirect(url_for('main.event'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_event = Event(event_name=title, details=details, place=place, time=time, category_id=category_id, owner_id=current_user.id)

    # add the new user to the database
    db.session.add(new_event)
    db.session.commit()


    return redirect('/event')


@main.route('/Dashboard')
@login_required
def Dashboard():
    users = db.session.execute('select * from user').fetchall()
    return render_template('Dashboard.html', users=users)