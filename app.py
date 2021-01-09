import os
from os.path import join, dirname, realpath


from flask import Flask, flash, render_template, request, redirect, url_for, send_file
# please note the import from `flask_uploads` - not `flask_reuploaded`!!
# this is done on purpose to stay compatible with `Flask-Uploads`
from flask_uploads import IMAGES, UploadSet, configure_uploads

# app = Flask(__name__)
# photos = UploadSet("photos", IMAGES)
# app.config["UPLOADED_PHOTOS_DEST"] = "static/img"
# app.config["SECRET_KEY"] = os.urandom(24)
# configure_uploads(app, photos)


# @app.route("/", methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST' and 'photo' in request.files:
#         photos.save(request.files['photo'])
#         flash("Photo saved successfully.")
#         return render_template('upload.html')
#     return render_template('upload.html')
    
    
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_uploads import configure_uploads, IMAGES, UploadSet

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/img/'

print('PATH: ', app.config['UPLOADED_IMAGES_DEST'])
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class Upload(FlaskForm):
    image = FileField('image')
    submit = SubmitField('Submit')

class Download(FlaskForm):
    submit = SubmitField('Download')


@app.route('/show/<picture>', methods=['GET', 'POST'])
def show(picture):
    download_form = Download()
    filename=app.config['UPLOADED_IMAGES_DEST']+picture
    
    if download_form.validate_on_submit(): 
        return send_file(filename, as_attachment=True)
    return render_template('show.html', pic=filename, form=download_form)


@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = Upload()

    if upload_form.validate_on_submit(): 
        filename = images.save(upload_form.image.data)
        print('show.html')
        return redirect(url_for('show', picture=filename))
        print('SAVED: ', filename)
    if request.method == 'GET':
        print('GET')

    return render_template('index.html', form=upload_form)


if __name__ == '__main__':
    app.run(debug=True)
