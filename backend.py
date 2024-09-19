from flask import Flask, request, jsonify
import os
import cv2
from flask_cors import CORS, cross_origin
import traceback
import base64

from src.cnnClassifier.utils.common import decodeImage
from src.cnnClassifier.pipeline.classification_with_XAI import PredictionPipeline
from src.chatbot_medical_assistant.agent import generate_response

# Set environment variables for UTF-8 encoding (optional):
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

app = Flask(__name__)
CORS(app)
# Supposons que vous ayez une liste de labels de classes, par exemple :
class_labels = ["Normal", "Adenocarcinoma Cancer"]  # Ajoutez vos labels de classes ici

# Initialisation de PredictionPipeline avec l'image d'entrée et les labels de classes
PREDICTION_PIPELINE = PredictionPipeline("input.png", class_labels)



@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        # Decode the incoming image data
        image_data = request.json['image']
        decoded_image_path = decodeImage(image_data, "input.png")
        
        # Run prediction and explanation generation
        class_prediction, overlay_image,explanation = PREDICTION_PIPELINE.predict()
        
        # Prepare the overlay image for transfer
        #overlay_image_path = "./react-frontend/public/output_overlay.png"
        #cv2.imwrite(overlay_image_path, overlay_image)
        _, buffer = cv2.imencode('.png', overlay_image)
        overlay_image_base64 = base64.b64encode(buffer).decode('utf-8')

        # Return results along with explanations
        result = {
            "prediction": class_prediction,
            "explanation": explanation,
            "overlay_image": overlay_image_base64
        }
        return jsonify(result), 200

    except Exception as e:
        traceback.print_exc()
        print("erreur",e)
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=['POST'])
@cross_origin()
def chat():
    """
    Route to handle chat requests from the frontend.
    Expects JSON input with 'message' (text) and optionally 'media' (file data).
    """
    try:
        print("Request data:", request.json)
        user_message = request.json.get('message')
        session_id=request.json.get('sessionId')
        print(user_message)
        if not user_message:
            return jsonify({"error": "Invalid input, 'message' field is required."}), 400
        
        # Call LangChain agent 
        reply = generate_response(user_message,session_id)
        
        return jsonify({"reply": reply}), 200
    
    except Exception as e:
        print("erreur",e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
