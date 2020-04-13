"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os,uuid
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, ProfileForm
from app.models import UserProfile
from werkzeug.utils import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

# @app.route('/profile/')
# def profile():
#     """Render the website's profile page."""
#     profileForm = ProfileForm()

#     if request.method == 'POST':
#         if profileForm.validate_on_submit():
#             fname = profileForm.fname.data
#             lname = profileForm.lname.data
#             gender = profileForm.gender.data
#             email = profileForm.email.data
#             location = profileForm.location.data
#             biography = profileForm.biography.data

#             photo = uploadForm.photo.data

#             filename = secure_filename(photo.filename)
#             photo.save(os.path.join(
#                 app.config['UPLOAD_FOLDER'], filename
#             ))

#             flash('New profile has been added.', 'success')
#             return redirect(url_for('home'))

#     return render_template('profile.html', form=profileForm)

@app.route('/profiles')
def profiles():
    """Render the all profiles in database"""
    images = get_uploaded_images()
    records = db.session.query(UserProfile).all()
    return render_template('profiles.html', images=images, records =records)

@app.route('/profile/<userid>')
def userProfile(userid):
    """Render the all profiles in database"""
    images = get_uploaded_images()
    record = UserProfile.query.filter_by(id=userid).first()
    return render_template('userProfile.html', images=images, record =record)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProfileForm()
    print(form.errors)

    if form.is_submitted():
        print ("submitted")

    if form.validate():
        print ("valid")

    print(form.errors)
    if request.method == "POST" and form.validate_on_submit():
        print("HELLO")
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        gender = request.form['gender']
        email = request.form['email']
        biography = request.form['biography']
        location = request.form['location']
        photo = form.photo.data
        fileName = uuid.uuid1().int 
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'],str(fileName)))
        user = UserProfile(firstName,lastName,gender,email,location,biography,fileName)
        db.session.add(user)
        db.session.commit()
        # remember to flash a message to the user
        flash("HELLO")
        return redirect(url_for('home'))  # they should be redirected to a secure-page route instead        
    return render_template("profile.html", form=form)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###
def get_uploaded_images():
    rootdir = os.getcwd()
    print(rootdir)
    lst = []
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            if file=='.gitkeep':
                continue
            lst.append(file)
    return lst



@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
