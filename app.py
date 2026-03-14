from flask import Flask, render_template, request, jsonify
import whisper
from transformers import pipeline
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

print("Loading models...")

model = whisper.load_model("base")
sentiment_pipeline = pipeline("sentiment-analysis")

print("Models loaded!")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "audio" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["audio"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # Transcribe
    result = model.transcribe(filepath)
    transcription = result["text"]

    # Sentiment
    sentiment = sentiment_pipeline(transcription)[0]

    return jsonify({
        "transcription": transcription,
        "sentiment": sentiment["label"],
        "score": round(sentiment["score"], 3)
    })


if __name__ == "__main__":
    app.run(debug=True)