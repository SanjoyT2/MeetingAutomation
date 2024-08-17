from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Enable CORS for all domains on all routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configure upload folder
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from app.resources.audio_processing import HealthCheck, AudioUpload, AudioTranscribe, AudioSummarize
    api.add_resource(HealthCheck, '/api/health')
    api.add_resource(AudioUpload, '/api/upload')
    api.add_resource(AudioTranscribe, '/api/transcribe/<string:filename>')
    api.add_resource(AudioSummarize, '/api/summarize')

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app
