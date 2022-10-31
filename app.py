import base64
from typing import io

from flask import Flask, request, render_template
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
from flask import jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #response시, 한글 깨짐 이슈 해결

label = {0:'고추탄저병',
         1:'고추흰가루병',
         2:'무검은무늬병',
         3:'무노균병',
         4:'배추검은썩음병',
         5:'배추노균병',
         6:'정상_고추',
         7:'정상_무',
         8:'정상_배추',
         9:'정상_콩',
         10:'정상_파',
         11:'콩불마름병',
         12:'콩점무늬병',
         13:'파검은무늬병',
         14:'파노균병',
         15:'파녹병'}

@app.route('/')
@app.route("/test")
def index():
    return "server test"

# 데이터 예측 처리
@app.route('/prediction')
def local_predict_test():
    model = load_model("C:/Users/Jo/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")

    image = Image.open("test_image/img.jpg")
    processed_image = preprocess_image(image, target_size=(224, 224))

    prediction = model.predict(processed_image).tolist()

    response = {
            'result': {
                'crop_name': label[np.argmax(prediction[0])],
                'percentage' : max(prediction[0])
            }
        }

    return flask.jsonify(response)

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image


@app.route("/prediction", methods=['POST'])
def predict():
    model = load_model("Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")
    # 바뀐 부분 시작
    plantType = request.form['plantType']
    # 바뀐 부분 끝

    # 바뀐 부분
    image = request.files['image']
    image.seek(0)
    encoded = Image.open(image)
    # 바뀐 부분 끝

    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

    # 바뀐 부분
    response = {
        'prediction': {
            'pestName': prediction[0][0],
            'pestPercentage': prediction[0][1]
        }
    }
    # 바뀐 부분 끝

    return jsonify(response)


if __name__ == '__main__':
    # Flask 서비스 스타트
    app.run(host='0.0.0.0',port=5000,debug=True)