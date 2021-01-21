from flask import Flask, request
import os
import numpy as np

app = Flask(__name__)
execution_path = os.getcwd()
glove_path = os.path.join(
    execution_path, "/models/categorisation/glove.6B.300d.txt")

embeddings_index = {}
with open(glove_path, encoding="utf8") as f:
    for line in f:
        values = line.split()
        word = values[0]
        embed = np.array(values[1:], dtype=np.float32)
        embeddings_index[word] = embed
print('Loaded %s word vectors.' % len(embeddings_index))

# Main Route:
@app.route('/keras', methods=['POST'])
def categorise():
    classification_json = request.get_json()
    category_data = classification_json["category_data"]
    best_prediction = classification_json["predictions"]["Best Prediction"]["Prediction"]
    mid_prediciton = classification_json["predictions"]["Mid Prediction"]["Prediction"]
    low_prediction = classification_json["predictions"]["Low Prediction"]["Prediction"]

    categories = {word: key for key, words in category_data.items()
                  for word in words}
    # Embeddings for available words
    data_embeddings = {key: value for key,
                       value in embeddings_index.items() if key in categories.keys()}

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

    def process(query):
        query_embed = embeddings_index[query.lower()]
        scores = {}
        highest_key = {}
        for word, embed in data_embeddings.items():
            category = categories[word]
            dist = query_embed.dot(embed)
            dist /= len(category_data[category])
            scores[category] = scores.get(category, 0) + dist
            highest_key = max(scores, key=scores.get)
        return highest_key

    best_category = get_category(best_prediction)
    mid_category = get_category(mid_prediciton)
    low_category = get_category(low_prediction)

    category_json = {
        "Best Prediction Category": best_category,
        "Mid Prediction Category": mid_category,
        "Low Prediction Category": low_category
    }

    return category_json

#ImageAI Route
@app.route('/imageai', methods=['POST'])
def categorise_imageai():
    imageai_objects_json = request.get_json()
    category_data = imageai_objects_json["category_data"]
    if imageai_objects_json["predictions"] == None:
        return {"Error": "COULD NOT FIND SUITABLE CLASSIFICIATION VIA IMAGEAI"}
    else:
        length = len(imageai_objects_json["predictions"])
        best_prediction = imageai_objects_json["predictions"]["Best Prediction"]
    
    if length > 1:
        mid_prediction = imageai_objects_json["predictions"]["Mid Prediction"]
    else:
        mid_prediction = None
    if length > 2:
        low_prediction = imageai_objects_json["predictions"]["Low Prediction"]
    else:
        low_prediction = None

    categories = {word: key for key, words in category_data.items()
                  for word in words}
    # Embeddings for available words
    data_embeddings = {key: value for key,
                       value in embeddings_index.items() if key in categories.keys()}

    def get_imageai_category(query):
        result = None
        # Try to process the query without modification
        try:
            result = process_imageai(query)
            return result
        except KeyError:
            pass
        # Try to join the word
        try:
            result = process_imageai(query.replace("_", ""))
            return result
        except KeyError:
            pass
        # Try to split string on underscore and take last word
        try:
            result = process_imageai(query.split("_")[-1])
            return result
        except KeyError:
            pass
        # Try to split string on underscore and take first word
        try:
            result = process_imageai(query.split("_")[0])
            return result
        except KeyError:
            pass

        return "NOT_CATEGORISED"

    def process_imageai(query):
        query_embed = embeddings_index[query.lower()]
        scores = {}
        highest_key = {}
        for word, embed in data_embeddings.items():
            category = categories[word]
            dist = query_embed.dot(embed)
            dist /= len(category_data[category])
            scores[category] = scores.get(category, 0) + dist
            highest_key = max(scores, key=scores.get)
        return highest_key

    best_category = get_imageai_category(best_prediction)
    if mid_prediction != None:
        mid_category = get_imageai_category(mid_prediction)
    else:
        mid_category = None
    if low_prediction != None:
        low_category = get_imageai_category(low_prediction)
    else:
        low_category = None

    category_json = {
        "Best Prediction Category": best_category
    }
    if mid_category != None:
        category_json["Mid Prediction Category"] = mid_category
    if low_category != None:
        category_json["Low Prediction Category"] = low_category

    return category_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060)