import os
# from os.path import join, dirname, realpath
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, send_file
from flask_uploads import IMAGES, UploadSet, configure_uploads
    
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_uploads import configure_uploads, IMAGES, UploadSet



# import some common libraries
import numpy as np
import os
# from google.colab.patches import cv2_imshow
# from PIL import Image



# import some common detectron2 utilities
from utils.model import run_model, get_model

##################
### Detectron2 ###
##################


################
### Fask APP ###
################
app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'app/static/img/'
app.config['PREFERRED_URL_SCHEME'] = 'https'

images = UploadSet('images', IMAGES)
configure_uploads(app, images)

class Upload(FlaskForm):
    image = FileField('image')
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
                    #wait_time=0.1,
                    # fig_size=(5,5),
                    win_name=processed_filename,
                    # bbox_color=(72, 101, 241),
                    # text_color=(72, 101, 241),
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
        print('send_file############processed_img:', processed_img)
        print(app.root_path, app.config['UPLOADED_IMAGES_DEST'])
        return send_file('/flask_detect/app/static/img/'+processed_filename, as_attachment=True)
        # return send_from_directory(app.config['UPLOADED_IMAGES_DEST'],
        #                        processed_filename, as_attachment=True)
    return render_template('show.html', pic=filename, form=download_form)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=False,use_reloader=True)


