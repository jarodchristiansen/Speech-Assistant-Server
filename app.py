from flask import Flask, request, jsonify
import os
import tempfile
import speech_recognition as sr

app = Flask(__name__)

# Initialize the recognizer
recognizer = sr.Recognizer()

@app.route('/recognize-speech', methods=['POST'])
def recognize_speech():
    try:
        # Check if a WAV file is provided in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']

        # Check if the file has a valid extension (e.g., .wav)
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            file.save(temp_file.name)

        # Perform speech recognition on the saved WAV file
        with sr.AudioFile(temp_file.name) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)

        # Remove the temporary file
        os.remove(temp_file.name)

        return jsonify({"recognized_text": text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()