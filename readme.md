# Audio Processing API

This Flask-based API provides endpoints for uploading audio files, transcribing them, and generating summaries.

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/audio-processor-api.git
   cd audio-processor-api
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:

   - Create a `.env` file in the root directory
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`

5. Run the application:
   ```
   python run.py
   ```

## API Endpoints

1. Upload an audio file:

   ```
   POST /api/upload
   Content-Type: multipart/form-data
   file: [audio file]
   ```

2. Transcribe an uploaded file:

   ```
   GET /api/transcribe/<filename>
   ```

3. Summarize text:
   ```
   POST /api/summarize
   Content-Type: application/json
   {
     "text": "transcription text here"
   }
   ```

## Usage Example

Using curl:

```bash
# Upload file
curl -X POST -F "file=@path/to/your/audio.mp3" http://localhost:5000/api/upload

# Transcribe file
curl http://localhost:5000/api/transcribe/audio.mp3

# Summarize text
curl -X POST -H "Content-Type: application/json" -d '{"text":"Your transcription text here"}' http://localhost:5000/api/summarize
```

## Note

This application is set up to process only the first 3 chunks of audio (approximately 3 minutes) for testing purposes. Adjust the `max_chunks` parameter in `app/services/audio_service.py` to process more or less of the audio file.

## Security

The `.env` file containing your API key is listed in `.gitignore` and should never be committed to the repository. Each developer should create their own `.env` file locally with their API key.
