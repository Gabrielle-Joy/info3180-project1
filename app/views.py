"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from app.forms import ProfileForm
from app.models import UserProfile


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


@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProfileForm()
    if request.method == "POST":
        # change this to actually validate the entire form submission
        # and not just one field
        if form.validate():
            firstName = request.form['firstname']
            lastName = request.form['lastName']
            gender = request.form['gender']
            email = request.form['email']
            biography = request.form['biography']
            profilePicture = request.form['profilePicture'].data
            fileName = hashlib.md5(profilePicture.tobytes()).hexdigest()
            profilePicture.save(os.path.join(app.config['UPLOAD_FOLDER'],fileName))
            print(fileName)
            user = UserProfile(firstName,lastName,gender,email,biography,fileName)
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
