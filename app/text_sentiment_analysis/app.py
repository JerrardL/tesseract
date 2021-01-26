from flask import Flask, request, jsonify

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

app = Flask(__name__)
sid = SentimentIntensityAnalyzer()

@app.route('/', methods=['POST'])
def text_sentiment():
    extraction = request.get_json()
    text_extraction = extraction["text"]
    pos =sid.polarity_scores(text_extraction)['pos']
    neg =sid.polarity_scores(text_extraction)['neg'] 
    neu =sid.polarity_scores(text_extraction)['neu']

    sentiment = {
        "positive": pos,
        "negative": neg,
        "neutral": neu
    }
    return jsonify({"text": sentiment})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5553)

