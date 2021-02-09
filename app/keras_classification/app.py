from flask import Flask, request

import numpy as np
import io
import json
import traceback

from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.python.keras.utils import data_utils
from PIL import Image

app = Flask(__name__)
model = VGG16(include_top=True, classes=1000,
              weights='/models/classification/keras/models/vgg16_weights_tf_dim_ordering_tf_kernels.h5')

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
        return {"Error": f"COULD NOT CLASSIFY IMAGE: {traceback.format_exc()}"}


def decode_predictions(preds, top=5):
  CLASS_INDEX = None
  if len(preds.shape) != 2 or preds.shape[1] != 1000:
    raise ValueError('`decode_predictions` expects '
                     'a batch of predictions '
                     '(i.e. a 2D array of shape (samples, 1000)). '
                     'Found array with shape: ' + str(preds.shape))
  if CLASS_INDEX is None:
    fpath = data_utils.get_file(
        'imagenet_class_index.json',
        None,
        cache_subdir='models',
        file_hash='c2c37ea517e94d9795004a39431a14cb',
        cache_dir='/models/classification/keras')
    with open(fpath) as f:
      CLASS_INDEX = json.load(f)
  results = []
  for pred in preds:
    top_indices = pred.argsort()[-top:][::-1]
    result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
    result.sort(key=lambda x: x[2], reverse=True)
    results.append(result)
  return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)