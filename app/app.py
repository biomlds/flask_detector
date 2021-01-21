from flask import Flask, render_template, redirect, url_for, send_from_directory, send_file
from flask_uploads import IMAGES, UploadSet, configure_uploads    
from flask_wtf import FlaskForm
# from wtforms import FileField, SubmitField
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

# from wtforms.validators import FileAllowed, FileRequired
from flask_uploads import configure_uploads, IMAGES, UploadSet

import numpy as np
from utils.model import run_model, get_model

################
### Fask APP ###
################
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/img/'
app.config['PREFERRED_URL_SCHEME'] = 'https'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class Upload(FlaskForm):
    image = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')

class Download(FlaskForm):
    submit = SubmitField('Download')

@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = Upload()

    if upload_form.validate_on_submit(): 
        filename = images.save(upload_form.image.data)
        processed_filename = f"detected_{filename}"

        img = f"{app.config['UPLOADED_IMAGES_DEST']}{filename}"
        processed_img = f"{app.config['UPLOADED_IMAGES_DEST']}{processed_filename}"
        print('UPLOADED_IMAGES_DEST', app.config['UPLOADED_IMAGES_DEST'])
        print('processed_img: ', processed_img, '##################')
        model, result = run_model(img=img)
        model.show_result(img, result, score_thr=0.5, show=False,
                    win_name=processed_filename,
                    out_file=processed_img) 

        return redirect(url_for('show', picture=filename))

    return render_template('index.html', form=upload_form)
    
@app.route('/show/<picture>', methods=['GET', 'POST'])
def show(picture):
    download_form = Download()
    
    filename = f"{picture}"
    processed_filename = f"detected_{picture}"
    img = f"{app.config['UPLOADED_IMAGES_DEST']}{filename}"
    processed_img = f"{app.config['UPLOADED_IMAGES_DEST']}{processed_filename}"

    if download_form.validate_on_submit():
        return send_file(app.config['UPLOADED_IMAGES_DEST']+processed_filename, as_attachment=True)
    return render_template('show.html', pic=filename, form=download_form)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True,use_reloader=True)


