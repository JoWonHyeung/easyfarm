from fastapi import FastAPI, UploadFile, File, Form, Response
from io import BytesIO
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from PIL import Image
from monitoring import instrumentator
import numpy as np


def model_load():
    # server model path
    model_path = "/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5"
    fa_path = "/Al_Flask_API_Server/model/fa_xception_unfreeze.h5"
    gochu_path = "/Al_Flask_API_Server/model/gochu_xception_unfreeze.h5"
    kong_path = "/Al_Flask_API_Server/model/kong_xception_unfreeze.h5"
    mu_path = "/Al_Flask_API_Server/model/mu_xception_fine_tuning.h5"
    bachu_path = "/Al_Flask_API_Server/model/bachu_xception_fine_tuning.h5"

    # local model path
    # model_path = "C:/Users/Jo/capstone/model/xception_epoch10_fine_tuning.h5"
    # fa_path = "C:/Users/Jo/capstone/model/fa_xception_unfreeze.h5"
    # gochu_path = "C:/Users/Jo/capstone/model/gochu_xception_unfreeze.h5"
    # kong_path = "C:/Users/Jo/capstone/model/kong_xception_unfreeze.h5"
    # mu_path = "C:/Users/Jo/capstone/model/mu_xception_fine_tuning.h5"
    # bachu_path = "C:/Users/Jo/capstone/model/bachu_xception_fine_tuning.h5"

    model = load_model(model_path)
    fa_model = load_model(fa_path)
    gochu_model = load_model(gochu_path)
    kong_model = load_model(kong_path)
    mu_model = load_model(mu_path)
    bachu_model = load_model(bachu_path)

    return model, fa_model, gochu_model, kong_model, mu_model, bachu_model


label = {
    0: '고추탄저병',
    1: '고추흰가루병',
    2: '무검은무늬병',
    3: '무노균병',
    4: '배추검은썩음병',
    5: '배추노균병',
    6: '정상_고추',
    7: '정상_무',
    8: '정상_배추',
    9: '정상_콩',
    10: '정상_파',
    11: '콩불마름병',
    12: '콩점무늬병',
    13: '파검은무늬병',
    14: '파노균병',
    15: '파녹병'}

gochu_label = {
    0: '고추탄저병',
    1: '고추흰가루병',
    2: '정상_고추'
}

mu_label = {
    0: '무검은무늬병',
    1: '무노균병',
    2: '정상_무'
}

bachu_label = {
    0: '배추검은썩음병',
    1: '배추노균병',
    2: '정상_배추'
}

fa_label = {
    0: '정상_파',
    1: '파검은무늬병',
    2: '파노균병'
}

kong_label = {
    0: '정상_콩',
    1: '콩불마름병',
    2: '콩점무늬병'
}

model, fa_model, gochu_model, kong_model, mu_model, bachu_model = model_load()

app = FastAPI()

instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)

class PredictionResult:
    pestName: str
    pestPercentage: float


@app.get('/')
def root_route():
    return {"error": "you must add url /prediction "}


@app.post('/prediction',response_model=PredictionResult)
async def prediction_route(image: UploadFile = File(...), response: Response = None):
    contents = await image.read()
    img = Image.open(BytesIO(contents))

    processed_image = preprocess_image(img, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

    result = {
        'result': {
            'pestName': label[np.argmax(prediction[0])],
            'pestPercentage': max(prediction[0])
        }
    }
    response.headers['pestName'] = str(np.argmax(prediction[0]))
    response.headers['pestPercentage'] = max(prediction[0])

    return PredictionResult


@app.post('/prediction/version2')
async def prediction_test(image: UploadFile = File(...), plantType: str = Form(...)):
    contents = await image.read()
    img = Image.open(BytesIO(contents))

    processed_image = preprocess_image(img, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

    response = ""
    if plantType != label_to_crop(label[np.argmax(prediction[0])]):
        if plantType == "고추":
            gochu_pred = gochu_model.predict(processed_image).tolist()
            response = {
                'result': {
                    'pestName': gochu_label[np.argmax(gochu_pred[0])],
                    'pestPercentage': max(gochu_pred[0])
                }
            }
        elif plantType == "배추":
            bachu_pred = bachu_model.predict(processed_image).tolist()
            response = {
                'result': {
                    'pestName': bachu_label[np.argmax(bachu_pred[0])],
                    'pestPercentage': max(bachu_pred[0])
                }
            }
        elif plantType == "파":
            fa_pred = fa_model.predict(processed_image).tolist()
            response = {
                'result': {
                    'pestName': fa_label[np.argmax(fa_pred[0])],
                    'pestPercentage': max(fa_pred[0])
                }
            }
        elif plantType == "콩":
            kong_pred = kong_model.predict(processed_image).tolist()
            response = {
                'result': {
                    'pestName': kong_label[np.argmax(kong_pred[0])],
                    'pestPercentage': max(kong_pred[0])
                }
            }
        elif plantType == "무":
            mu_pred = mu_model.predict(processed_image).tolist()
            response = {
                'result': {
                    'pestName': mu_label[np.argmax(mu_pred[0])],
                    'pestPercentage': max(mu_pred[0])
                }
            }
        else:
            response = {
                'result' : {
                    'status': 'plantType error'
                }
            }
    else:
        response = {
            'result': {
                'pestName': label[np.argmax(prediction[0])],
                'pestPercentage': max(prediction[0])
            }
        }
    return response


def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image


def label_to_crop(crop):
    if crop == "고추흰가루병" or crop == "고추탄저병" or crop == "정상_고추":
        return "고추"
    elif crop == "무검은무늬병" or crop == "무노균병" or crop == "정상_무":
        return "무"
    elif crop == "배추검은썩음병" or crop == "배추노균병" or crop == "정상_무":
        return "배추"
    elif crop == "콩점무늬병" or crop == "콩불마름병" or crop == "정상_콩":
        return "콩"
    elif crop == "파녹병" or crop == "파노균병" or crop == "파검은무늬병" or crop == "정상_파":
        return "파"
    else:
        return "error"
