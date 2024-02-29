from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from app import app
from app.models.user import User

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("home.html", users=User.get_all())

@app.route('/user/login', methods=['POST'])
def login():
    email_address = request.form['email_address']
    password = request.form['password']

    user = User.get_by_email(email_address)

    if not user:
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password, password): # incoming password second
        return redirect("/")
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/user/<int:id>')
def view_user(id):
    user = User.get_by_id(id)
    return render_template("my_pets.html", user = user)

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/user/register", methods=["POST"])
def register():
    """
        Give credentials
        validation
        hash password
        add to database
    """

    if not User.validate_new_user(request.form):
        return redirect("/")
    
    hashed_password = bcrypt.generate_password_hash(request.form['password'])

    User.create({
        **request.form,
        "password": hashed_password
    })

    flash("Thank you for registering")
    return redirect("/")
