from flask import Flask, request, jsonify

from analyser import SentimentIntensityAnalyzer

app = Flask(__name__)
sid = SentimentIntensityAnalyzer()

@app.route('/', methods=['POST'])
def text_sentiment():
    extraction = request.get_json()
    text_extraction = extraction["text"]
    pos =sid.polarity_scores(text_extraction)['pos']
    neg =sid.polarity_scores(text_extraction)['neg'] 
    neu =sid.polarity_scores(text_extraction)['neu']
    com =sid.polarity_scores(text_extraction)['compound']

    sentiment = {
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "compound": com
    }
    return jsonify({"text": sentiment})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5553)

