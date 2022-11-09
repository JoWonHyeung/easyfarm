import base64
from typing import io

from flask import Flask, request, render_template
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
from flask import jsonify
from io import BytesIO
import io

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

# Local Test
# @app.route('/prediction')
# def local_predict_test():
#     model = load_model("C:/Users/Jo/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")
#
#     image = Image.open("test_image/img.jpg")
#     processed_image = preprocess_image(image, target_size=(224, 224))
#
#     prediction = model.predict(processed_image).tolist()
#
#     response = {
#             'result': {
#                 'crop_name': label[np.argmax(prediction[0])],
#                 'percentage' : max(prediction[0])
#             }
#         }
#
#     return flask.jsonify(response)

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image



@app.route("/prediction",methods=['POST'])
def predict():
    model = load_model("/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")

    #plantType = request.form['plantType']

    image = request.files['image'].read()

    image = Image.open(io.BytesIO(image))
    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

    # 바뀐 부분
    response = {
                'result': {
                    'pestName': label[np.argmax(prediction[0])],
                    'pestPercentage' : max(prediction[0])
                }
            }
    return jsonify(response)


if __name__ == '__main__':
    # Flask 서비스 스타트
    app.run(host='0.0.0.0',port=5000,debug=True)