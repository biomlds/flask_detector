import os
# from os.path import join, dirname, realpath
from flask import Flask, flash, render_template, request, redirect, url_for, send_file
from flask_uploads import IMAGES, UploadSet, configure_uploads
    
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_uploads import configure_uploads, IMAGES, UploadSet


# Some basic setup for Detectron2:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os
# from google.colab.patches import cv2_imshow
# from PIL import Image



# import some common detectron2 utilities
import torch
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

from app.utils.model import get_model, run_model

##################
### Detectron2 ###
##################

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu").type

predictor = get_model(tresh=0.5, device=device)

################
### Fask APP ###
################
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
    processed_img = run_model(picture, app.config['UPLOADED_IMAGES_DEST'])
    filename=app.config['UPLOADED_IMAGES_DEST']+processed_img
    
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
