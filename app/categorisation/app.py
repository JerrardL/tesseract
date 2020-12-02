from flask import Flask, request


app = Flask(__name__)

# Main Route:
# Use POST method with binary and file to upload via Postman
@app.route('/', methods=['POST'])
def categorise():
    speech = request.get_data()
    # category = engine.run(speech)
    # return jsonify({"text": text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)