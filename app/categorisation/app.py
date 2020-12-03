from flask import Flask, request

import numpy as np


app = Flask(__name__)

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def categorise():
    classification_json = request.get_json()
    category_data = classification_json["category_data"]
    best_prediction = classification_json["predictions"]["Best Prediction"]["Prediction"]
    mid_prediciton = classification_json["predictions"]["Mid Prediction"]["Prediction"]
    low_prediction = classification_json["predictions"]["Low Prediction"]["Prediction"]

    categories = {word: key for key, words in category_data.items() for word in words}

    embeddings_index = {}
    with open('/glove/glove.6B.300d.txt', encoding="utf8") as f:
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

    def process(query):
        query_embed = embeddings_index[query.lower()]
        scores = {}
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6060)