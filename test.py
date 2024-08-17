import requests
import time
import os

# Base URL of your Flask app
BASE_URL = 'http://localhost:5000'


def test_health():
    url = f'{BASE_URL}/api/health'
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Health Check Response:", response.json())
    except requests.exceptions.RequestException as e:
        print("Health Check Failed:", e)


def upload_audio(file_path):
    url = f'{BASE_URL}/api/upload'
    if not os.path.exists(file_path):
        print(f"Error: File not found - {file_path}")
        return None
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            print("Upload Response:", response.json())
            return response.json().get('filename')
        except requests.exceptions.RequestException as e:
            print("Upload Failed:", e)
            return None


def transcribe_audio(filename):
    url = f'{BASE_URL}/api/transcribe/{filename}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        print("Transcribe Response:", result)
        return result.get('transcription')
    except requests.exceptions.RequestException as e:
        print("Transcription Failed:", e)
        return None


def summarize_text(text):
    url = f'{BASE_URL}/api/summarize'
    data = {'text': text}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print("Summarize Response:", response.json())
        return response.json().get('summary')
    except requests.exceptions.RequestException as e:
        print("Summarization Failed:", e)
        return None


def write_to_file(content, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Content written to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")


def main():
    test_health()

    audio_file_path = 'test.m4a'  # Replace with your actual file path

    print("\nUploading audio file...")
    filename = upload_audio(audio_file_path)

    if filename:
        print(f"\nAudio file uploaded successfully. Filename: {filename}")

        print("\nTranscribing audio...")
        transcription = transcribe_audio(filename)

        if transcription:
            print("\nTranscription successful. Writing to file...")
            write_to_file(transcription, 'transcription.txt')

            print("\nSummarizing transcription...")
            summary = summarize_text(transcription)
            if summary:
                print("\nSummarization successful. Writing to file...")
                write_to_file(summary, 'summary.txt')
            else:
                print("Summarization failed or returned empty.")
        else:
            print("Transcription failed or returned empty.")
    else:
        print("Audio upload failed.")


if __name__ == '__main__':
    main()
