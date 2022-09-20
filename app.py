from flask import Flask, request, render_template
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import pandas as pd
import tensorflow as tf
import os
from scipy import misc

pd.options.display.float_format = '{:.5f}'.format

app = Flask(__name__)

#데이터 load
model = load_model('model/keras_model.h5')

@app.route('/')
@app.route("/test")
def index():
    return "Server Test"

# 데이터 예측 처리
@app.route('/prediction')
def make_prediction():
    data = {"success": False};

    image = Image.open("test_image/배추노균병.png")
    image = prepare_image(image, target=(224, 224))

    preds = model.predict(image)
    return str(np.argmax(preds[0]))

    # if request.method == 'POST':
    #     pass

def prepare_image(image, target):
    # image mode should be "RGB"
    if image.mode != "RGB":
        image = image.convert("RGB");

    # resize for model
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return it
    return image

if __name__ == '__main__':

    # Flask 서비스 스타트
    app.run(port=8000)
    app.run(host='0.0.0.0',port=8000)
    app.run(host='172.31.90.151',port=8000)