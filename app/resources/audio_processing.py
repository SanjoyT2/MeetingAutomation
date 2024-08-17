from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from flask import current_app
from werkzeug.utils import secure_filename
import os
from app.services.audio_service import split_audio, transcribe_audio, summarize_text
from dotenv import load_dotenv

load_dotenv()


class HealthCheck(Resource):
    def get(self):
        return {
            'status': 'OK',
            'message': 'Server is running',
            'environment': os.getenv('FLASK_ENV', 'development'),
            'chunk_limit': os.getenv('CHUNK_LIMIT', '3')
        }, 200


class AudioUpload(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage,
                           location='files', required=True)
        args = parse.parse_args()

        audio_file = args['file']
        if audio_file:
            filename = secure_filename(audio_file.filename)
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(file_path)
            return {'message': 'File uploaded successfully', 'filename': filename}, 200
        return {'message': 'No file uploaded'}, 400


class AudioTranscribe(Resource):
    def get(self, filename):
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return {'message': 'File not found'}, 404

        try:
            chunks = split_audio(file_path)
            full_transcription = ""
            for chunk in chunks:
                transcription = transcribe_audio(chunk)
                full_transcription += transcription + " "
                os.remove(chunk)

            return {
                'transcription': full_transcription,
                'chunks_processed': len(chunks),
                'environment': os.getenv('FLASK_ENV', 'development'),
                'chunk_limit': os.getenv('CHUNK_LIMIT', '3')
            }, 200
        except Exception as e:
            return {'message': str(e)}, 500


class AudioSummarize(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('text', type=str, required=True)
        args = parse.parse_args()

        text = args['text']
        try:
            summary = summarize_text(text)
            return {'summary': summary}, 200
        except Exception as e:
            return {'message': str(e)}, 500
