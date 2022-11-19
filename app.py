from typing import io
from flask import Flask, request,jsonify
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from PIL import Image
import numpy as np
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

#server model load
model = load_model("/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")
#local model load
#model = load_model("C:/Users/Jo/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")

@app.route('/')
def index():
    return "capstone server"

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
    #plantType = request.form['plantType']

    image = request.files['image'].read()

    image = Image.open(io.BytesIO(image))
    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

    response = {
                'result': {
                    'pestName': label[np.argmax(prediction[0])],
                    'pestPercentage' : max(prediction[0])
                }
            }

    return jsonify(response)

# @app.route("/prediction/test")
# def predictLayer2():
#     #server model load
#     model = load_model("/Al_Flask_API_Server/model/gochu_xception_unfreeze.h5")
#     #local model load
#     #model = load_model("C:/Users/Jo/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5")
#
#     #사용자 입력 작물
#     plantType = request.form['plantType']
#
#     #image processing
#     image = request.files['image'].read()
#
#     image = Image.open(io.BytesIO(image))
#     processed_image = preprocess_image(image, target_size=(224, 224))
#
#     #predict
#     prediction = model.predict(processed_image).tolist()
#
#     #result label -> crop name
#     pestNameToCrop = label_to_crop(label[np.argmax(prediction[0])])
#     print("result label to crop name : " + pestNameToCrop)
#
#     # 입력 작물과 1차 layer를 거친 결과로 나온 작물이 다른 경우 작물별 학습 진행
#     if plantType != pestNameToCrop:
#         if plantType == "파":
#             gochu_model = load_model("/Al_Flask_API_Server/model/gochu_xception_unfreeze.h5")
#             prediction = gochu_model.predict(processed_image).tolist()
#             response = {
#                 'resultLayer2': {
#                     'pestName': label[np.argmax(prediction[0])],
#                     'pestPercentage': max(prediction[0])
#                 }
#             }
#             return jsonify(response)
#         elif plantType == "배추":
#             pass
#         elif plantType == "콩":
#             pass
#         elif plantType == "고추":
#             pass
#         elif plantType == "무":
#             pass
#         else:
#             print("PlantType Error")
#
#     response = {
#                 'result': {
#                     'pestName': label[np.argmax(prediction[0])],
#                     'pestPercentage' : max(prediction[0])
#                 }
#             }
#
#     return jsonify(response)

def label_to_crop(crop):
    if crop == "고추흰가루병" or crop == "고추탄저병" or crop == "정상_고추": return "고추"
    elif crop == "무검은무늬병" or crop == "무노균병" or crop == "정상_무": return "무"
    elif crop == "배추검은썩음병" or crop == "배추노균병" or crop == "정상_무": return "배추"
    elif crop == "콩점무늬병" or crop == "콩불마름병" or crop == "정상_콩": return "콩"
    elif crop == "파녹병" or crop == "파노균병" or crop == "파검은무늬병" or crop == "정상_파": return "파"
    else: return "error"

#Server start
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)