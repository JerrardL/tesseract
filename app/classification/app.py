from flask import Flask, request

import numpy as np
import io
import os
os.environ['KERAS_HOME'] = os.path.join('/models/classification/', 'keras')
from tensorflow.keras.applications.vgg16 import VGG16

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.python.framework.errors_impl import InvalidArgumentError
from PIL import Image

app = Flask(__name__)
model = VGG16(include_top=True, classes=1000, weights='imagenet')

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def classify():
    image_data = request.get_data()

    img = Image.open(io.BytesIO(image_data))
    img = img.resize((224, 244), Image.ANTIALIAS)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    try:

        preds = model.predict(x)
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        prediction = decode_predictions(preds, top=3)[0][0][1]
        confidence = decode_predictions(preds, top=3)[0][0][2]
        mid_pred = decode_predictions(preds, top=3)[0][1][1]
        mid_con = decode_predictions(preds, top=3)[0][1][2]
        low_pred = decode_predictions(preds, top=3)[0][2][1]
        low_con = decode_predictions(preds, top=3)[0][2][2]
        prediction_json = {
            "Best Prediction": {
                "Prediction": prediction,
                "Confidence": str(confidence)
            },
            "Mid Prediction": {
                "Prediction": mid_pred,
                "Confidence": str(mid_con)
            },
            "Low Prediction": {
                "Prediction": low_pred,
                "Confidence": str(low_con)
            }
        }
        return prediction_json
    
    except:
        return {"Error": "COULD NOT CLASSIFY IMAGE"}




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)