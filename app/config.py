import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max-limit
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    CHUNK_LIMIT = int(os.environ.get('CHUNK_LIMIT', 3))
