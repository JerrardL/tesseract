import numpy as np
import json

data = {
    'Violent': ['rifle', 'handgun', 'firearm', 'blade', 'knife', 'blood'],
    'Location': ['beach', 'park', 'forest', 'river', 'garden', 'mountain'],
    'Dogs': ['poodle', 'labrador', 'great dane', 'chihuahua', 'pug', 'bulldog'],
    'Vehicle': ['car', 'van', 'truck', 'hatchback', 'bus', 'lorry'],
    'People': ['man', 'woman', 'child', 'baby', 'girl', 'boy'],
    'Clothing': ['jacket', 'shorts', 'skirt', 'trousers', 'hat', 'shirt'],
    'Activities': ['swimming', 'running', 'walking', 'cycling', 'jogging', 'golfing'],
}

categories = {word: key for key, words in data.items() for word in words}

embeddings_index = {}
with open('./glove.6B.300d.txt', encoding="utf8") as f:
  for line in f:
    values = line.split()
    word = values[0]
    embed = np.array(values[1:], dtype=np.float32)
    embeddings_index[word] = embed
print('Loaded %s word vectors.' % len(embeddings_index))
# Embeddings for available words
data_embeddings = {key: value for key, value in embeddings_index.items() if key in categories.keys()}

def get_category(query):
    
    result = None

    # Try to process the query without modification
    try:
        result = process(query)
        return result
    except KeyError:
        pass

    # Try to join the word
    try:
        result = process(query.replace("_", ""))
        return result
    except KeyError:
        pass

    # Try to split string on underscore and take last word
    try:
        result = process(query.split("_")[-1])
        return result
    except KeyError:
        pass

    # Try to split string on underscore and take first word
    try:
        result = process(query.split("_")[0])
        return result
    except KeyError:
        pass

    return "NOT_CATEGORISED"

# Processing the query
def process(query):
    query_embed = embeddings_index[query.lower()]
    scores = {}
    for word, embed in data_embeddings.items():
        category = categories[word]
        dist = query_embed.dot(embed)
        dist /= len(data[category])
        scores[category] = scores.get(category, 0) + dist
        highest_key = max(scores, key=scores.get)
    return highest_key

## Keras with InceptionResNetV2 ###

from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_resnet_v2 import preprocess_input, decode_predictions

model = InceptionResNetV2(classes=1000, weights='imagenet')

img_path = '../uploaded/fatherson.jpg'
img = image.load_img(img_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)

preds = model.predict(x)
# decode the results into a list of tuples (class, description, probability)
# (one such list for each sample in the batch)
prediction = decode_predictions(preds, top=3)[0][0][1]
confidence = decode_predictions(preds, top=3)[0][0][2]
mid_pred = decode_predictions(preds, top=3)[0][1][1]
mid_con = decode_predictions(preds, top=3)[0][1][2]
low_pred = decode_predictions(preds, top=3)[0][2][1]
low_con = decode_predictions(preds, top=3)[0][2][2]

category = get_category(prediction)
mid_cat = get_category(mid_pred)
low_cat = get_category(low_pred)
prediction_json = {
    "Best Prediction": {
        "Prediction": prediction,
        "Confidence": str(confidence),
        "Closest Category": category
    },
    "Mid Prediction": {
        "Prediction": mid_pred,
        "Confidence": str(mid_con),
        "Closest Category": mid_cat
    },
    "Low Prediction": {
        "Prediction": low_pred,
        "Confidence": str(low_con),
        "Closest Category": low_cat
    }
}
print(json.dumps(prediction_json))

#print('Predicted:', predicition)
#print(process(predicition))