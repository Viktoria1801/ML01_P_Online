import pickle
import numpy as np
from flask import Flask, request, jsonify

# Загружаем модель
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        features = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
