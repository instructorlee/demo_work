import os
from app import app
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask import Flask, session, render_template, request, redirect, flash, url_for, send_file
from app.decorators import login_required
from app.models.pet import Pet
from app.models.user import User

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# posting data is a 2 step process 1- server form, 2-process data from form
@app.route('/pet/add')
@login_required()
def get_add_pet_form(user):
    return render_template("add.html")

@app.route('/pet/add', methods=['POST'])
@login_required()
def add_pet(user):
     # check if the post request has the file part
    if 'pet_image' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['pet_image']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect("/pet/add")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        
    Pet.add({
        **request.form,
        'file_name': filename
    })
    return redirect("/dashboard")

@app.route('/pet/update/<int:id>')
@login_required()
def get_update_pet_form(user, id):
    pet = Pet.get_by_id(id)
    
    if 'update_form' in session:
        pet.name = session['update_form']['name']
        session.pop('update_form')

    if pet:
        if pet.owner.id != session['user_id']:
            return redirect("/user/logout")
    
    return render_template("update.html", pet=pet)

@app.route('/pet/update', methods=['POST'])
def update_pet():
    if not "user_id" in session:
        return redirect("/user/logout")
    
    pet = Pet.get_by_id(int(request.form['id']))

    if pet:
        if pet.owner.id != session['user_id']:
            return redirect("/user/logout")
    
    if int(request.form['happiness']) <= 0:
        flash("error")
        session['update_form'] = request.form
        return redirect(f"/pet/update/{pet.id}")
        
    Pet.update(request.form)
    return redirect('/dashboard')

@app.route('/pet/<int:id>')
def get_pet(id):
    return render_template('view.html', pet=Pet.get_by_id(id))

@app.route('/pet/delete/<int:id>')
def delete_pet(id):
    Pet.delete(id)

    return redirect('/dashboard')

@app.route('/pet/like/<int:id>')
def like_pet(id):
    
    Pet.like(id, session['user_id'])
    flash(f"Thank you for liking {Pet.get_by_id(id).name}!")

    return redirect(f"/pet/{id}")

@app.route('/pet/unlike/<int:id>')
def unlike_pet(id):
    
    Pet.unlike(id, session['user_id'])
    flash(f"Thank you for unliking {Pet.get_by_id(id).name}!")

    return redirect(f"/pet/{id}")

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash("Login to Access the Dashboard!")
        return redirect('/')
    
    time = "01/23/24, 17:57:43"
    time_val = datetime.strptime(time, "%m/%d/%y, %H:%M:%S")
    add_two = time_val + timedelta(hours = -22)
    print(add_two)

    return render_template("dashboard.html", pets=Pet.get_all(), user=User.get_by_id(session['user_id']))


@app.route('/pet/image/<int:id>')
def get_image(id):

    pet = Pet.get_by_id(id)
    return send_file(os.path.abspath(app.config['UPLOAD_FOLDER'] + '/' + pet.file_name), mimetype='image/png')
