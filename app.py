import os
import tempfile
from flask import Flask, request, jsonify
import whisper
import torch
from werkzeug.exceptions import RequestTimeout

# Utiliser tous les CPUs disponibles
torch.set_num_threads(4)

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp:
                file.save(temp.name)
                result = model.transcribe(temp.name)
            os.unlink(temp.name)
            return jsonify({"transcription": result["text"]})
    except RequestTimeout:
        return jsonify({"error": "Request timed out. The audio file might be too long or the server is overloaded."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
