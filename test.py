from fastapi import FastAPI, UploadFile, File
from io import BytesIO
from PIL import Image
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from PIL import Image
import numpy as np

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

#server model path
model_path = "/Al_Flask_API_Server/model/xception_epoch10_fine_tuning.h5"

model = load_model(model_path)

app = FastAPI()

@app.get('/')
def root_route():
    return {"error": "use GET /prediction instead of root route"}

# 데이터 준비
@app.post('/prediction')
async def prediction_route(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents))

    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image).tolist()

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