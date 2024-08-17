from pydub import AudioSegment
from openai import OpenAI
from pathlib import Path
import os
from flask import current_app
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def split_audio(file_path, chunk_length_ms=60000):
    print(f"Splitting {file_path} into chunks...")
    file_extension = Path(file_path).suffix.lower()

    if file_extension == '.mp3':
        audio = AudioSegment.from_mp3(file_path)
    elif file_extension == '.m4a':
        audio = AudioSegment.from_file(file_path, format="m4a")
    elif file_extension in ['.wav', '.wave']:
        audio = AudioSegment.from_wav(file_path)
    else:
        audio = AudioSegment.from_file(file_path)

    chunks = []
    chunk_limit = os.getenv('CHUNK_LIMIT', '3')
    chunk_limit = int(chunk_limit) if chunk_limit.lower() != 'none' else None

    for i, chunk in enumerate(audio[::chunk_length_ms]):
        if chunk_limit is not None and i >= chunk_limit:
            break
        chunk_name = os.path.join(
            current_app.config['UPLOAD_FOLDER'], f"chunk{i}.mp3")
        chunk.export(chunk_name, format="mp3")
        chunks.append(chunk_name)

    print(f"Created {len(chunks)} chunks.")
    return chunks


def transcribe_audio(audio_file):
    print(f"Transcribing {audio_file}...")
    with open(audio_file, "rb") as file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=file,
            language="en"
        )
    return transcription.text


def summarize_text(text):
    print("Summarizing transcription...")
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text with bullet points. Always provide the summary in English."},
            {"role": "user", "content": f"Please summarize the following text with bullet points in English:\n\n{text}"}
        ]
    )
    return response.choices[0].message.content
