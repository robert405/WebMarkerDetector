from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import render_template
from ArucoDetector import ArucoDetector
from Utils import readb64

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detectArucoMarker', methods=['POST'])
def detectArucoMarker():

    if not request.json or not 'data' in request.json:
        abort(400)

    detector = ArucoDetector()

    try:

        img = readb64(request.json['data'])
        ar = detector.detectAndCorrect(img)
        return jsonify({'result': "SUCCESS, Detector found 4 markers!"}), 200

    except:

        return jsonify({'result': "FAILURE, Detector did not found 4 markers!"}), 200



if __name__ == '__main__':
    app.run(host='132.203.114.102', port=8080)
