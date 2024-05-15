from flask import Flask, request, jsonify
from model import model

app = Flask(__name__)


@app.route('/process_image', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify(error='No image uploaded'), 400

        image = request.files['image']

        grade = model(image)

        return jsonify(grade=grade[0])
    except Exception as e:
        return jsonify(error=e), 500


if __name__ == '__main__':
    app.run(debug=True)
