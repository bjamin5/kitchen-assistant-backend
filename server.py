from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Recipe Chatbot API!"


@app.route('/fetch_recipe', methods=['POST'])
def fetch_recipe():
    data = request.json
    recipe_link = data.get('link')

    if not recipe_link:
        return jsonify({'error': 'No link provided'}), 400

    # Dummy implementation: In a real app, you would fetch the recipe content from the link.
    recipe_content = f"Fetched recipe content from {recipe_link}"

    return jsonify({'recipe': recipe_content}), 200


@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Dummy implementation: Replace this with actual transcription using Whisper AI.
    transcribed_text = "This is a transcribed text from the audio."

    return jsonify({'transcription': transcribed_text}), 200


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({'error': 'No query provided'}), 400

    # Dummy implementation: Replace this with actual ChatGPT API call.
    chatgpt_response = f"Response to the query: {user_query}"

    return jsonify({'response': chatgpt_response}), 200


if __name__ == '__main__':
    app.run(debug=True)
