from flask import Flask, request, jsonify
from model_utils import load_model, predict_class
import os

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "final_model.pth")
model = load_model(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_path = data.get("image_path")

    if not image_path or not os.path.exists(image_path):
        return jsonify({"error": "Image path invalide ou introuvable"}), 400

    try:
        result, confidence, probabilities = predict_class(model, image_path)
        return jsonify({
            "class": result,
            "confidence": confidence,
            "probabilities": probabilities
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
