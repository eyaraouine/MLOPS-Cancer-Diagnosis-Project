from flask import Flask, request, jsonify
import os
from flask_cors import CORS, cross_origin

from src.cnnClassifier.utils.common import decodeImage
from src.cnnClassifier.pipeline.classification import PredictionPipeline

# Set environment variables for UTF-8 encoding (optional):
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

app = Flask(__name__)
CORS(app)

# Create the PredictionPipeline instance outside of routes:
PREDICTION_PIPELINE = PredictionPipeline("input.png")

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decoded_image = decodeImage(image,"input.png")
    result = PREDICTION_PIPELINE.predict(decoded_image)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
