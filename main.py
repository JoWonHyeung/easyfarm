from fastapi import FastAPI, UploadFile, File, Form, status
from io import BytesIO
from keras_preprocessing.image import img_to_array
from PIL import Image
from monitoring import instrumentator
import numpy as np
from pydantic import BaseModel, Field
import constant.labelConstant as LabelConstant
import model.load.modelLoad as ModelLoad

model, fa_model, gochu_model, kong_model, mu_model, bachu_model = ModelLoad.modelLoad()

app = FastAPI()
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)

class PredictionResult(BaseModel):
    pestName: str = Field(..., description="pestName")
    pestPercentage: float = Field(..., description='pestPercentage')
    inputPlant: str = Field(..., description='inputPlant')
    class Config:
        orm_mode = True

@app.get('/')
def root_route():
    return {"error": "you must add url /prediction "}

@app.post('/prediction')
async def prediction(image: UploadFile = File(...), plantType: str = Form(...)):
    contents = await image.read()
    img = Image.open(BytesIO(contents))

    processedImage = preprocessImage(img, target_size=(224, 224))
    prediction = model.predict(processedImage).tolist()

    return responseDoubleLayerLogic(plantType, prediction, processedImage)

def responseDoubleLayerLogic(plantType, prediction, processedImage):
    if plantType != labelToCrop(LabelConstant.label[np.argmax(prediction[0])]):
        if plantType == "고추":
            gochu_pred = gochu_model.predict(processedImage).tolist()
            response = {
                'result': {
                    'pestName': LabelConstant.gochu_label[np.argmax(gochu_pred[0])],
                    'pestPercentage': max(gochu_pred[0]),
                    'status': status.HTTP_201_CREATED
                }
            }
        elif plantType == "배추":
            bachu_pred = bachu_model.predict(processedImage).tolist()
            response = {
                'result': {
                    'pestName': LabelConstant.bachu_label[np.argmax(bachu_pred[0])],
                    'pestPercentage': max(bachu_pred[0]),
                    'status': status.HTTP_201_CREATED
                }
            }
        elif plantType == "파":
            fa_pred = fa_model.predict(processedImage).tolist()
            response = {
                'result': {
                    'pestName': LabelConstant.fa_label[np.argmax(fa_pred[0])],
                    'pestPercentage': max(fa_pred[0]),
                    'status': status.HTTP_201_CREATED
                }
            }
        elif plantType == "콩":
            kong_pred = kong_model.predict(processedImage).tolist()
            response = {
                'result': {
                    'pestName': LabelConstant.kong_label[np.argmax(kong_pred[0])],
                    'pestPercentage': max(kong_pred[0]),
                    'status': status.HTTP_201_CREATED
                }
            }
        elif plantType == "무":
            mu_pred = mu_model.predict(processedImage).tolist()
            response = {
                'result': {
                    'pestName': LabelConstant.mu_label[np.argmax(mu_pred[0])],
                    'pestPercentage': max(mu_pred[0]),
                    'status': status.HTTP_201_CREATED
                }
            }
        else:
            response = {
                'result': {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'comment' : "you must check plantType name."
                }
            }
    else:
        response = {
            'result': {
                'pestName': LabelConstant.label[np.argmax(prediction[0])],
                'pestPercentage': max(prediction[0]),
                'status': status.HTTP_201_CREATED
            }
        }
    return response

def preprocessImage(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image

def labelToCrop(crop):
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





