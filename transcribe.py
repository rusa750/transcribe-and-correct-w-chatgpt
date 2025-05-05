import os
import shutil
from dotenv import load_dotenv
from openai import OpenAI
from pydub import AudioSegment

def transcribe():
    """
    Инициализирует OpenAI-клиент и возвращает функции для очистки, конвертации и транскрипции аудиофайлов.

    1) Загружает ключ API из файла .env и инициализирует клиента OpenAI.
    2) Внутри определяет и возвращает три вспомогательные функции:
    - Очистка временной рабочей папки (working).
    - Конвертация аудиофайлов в формат .wav.
    - Транскрипция аудиофайлов с возможной нарезкой и сохранением в формате .vtt.

    Returns:
        tuple:
            clear_working_directory (Callable[[str], None]): Функция для очистки временной рабочей папки.
            convert_to_wav (Callable[[str], str | None]): Функция конвертации аудиофайла в .wav.
            transcribe_audio_file (Callable[[str], str | None]): Функция транскрипции аудиофайла с сохранением результатов.
    """

    # Load environment variables
    load_dotenv()

    # Set your API key
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY not set in .env file")

    # Initialize OpenAI client
    client = OpenAI()

    def clear_working_directory(path="./working"):
        if os.path.exists(path):
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

    def convert_to_wav(file_path):
        try:
            if not file_path.endswith(".wav"):
                audio = AudioSegment.from_file(file_path)
                wav_file_path = file_path.rsplit(".", 1)[0] + ".wav"
                audio.export(wav_file_path, format="wav")
                return wav_file_path
            return file_path
        except Exception as e:
            print(f"Error converting file to .wav: {e}")
            return None

    def transcribe_audio_file(file_path):
        base_name = os.path.basename(file_path).rsplit(".", 1)[0]
        transcription_folder = f"./transcriptions/{base_name}"

        if os.path.exists(transcription_folder):
            print(f"⏭️📂 Folder {transcription_folder} already exists. Skipping the whole thing.")
            return None

        os.makedirs(transcription_folder, exist_ok=True)

        try:
            wav_file_path = convert_to_wav(file_path)
            if not wav_file_path:
                return None

            working_dir = "./working"
            os.makedirs(working_dir, exist_ok=True)

            model_id = "whisper-1"
            response_format = "vtt"

            def split_audio(file_path, max_size=25 * 1024 * 1024, verbose=True):
                audio = AudioSegment.from_file(file_path)
                duration_ms = len(audio)

                num_segments = (os.path.getsize(file_path) // max_size) + 1
                segment_duration_ms = duration_ms // num_segments

                segments = []
                for i in range(num_segments):
                    start = i * segment_duration_ms
                    end = duration_ms if i == num_segments - 1 else (i + 1) * segment_duration_ms
                    segment = audio[start:end]
                    segment_path = os.path.join(working_dir, f"segment_{i}.wav")
                    segment.export(segment_path, format="wav")
                    segments.append(segment_path)
                    if verbose:
                        print(f"🎧 Segment {i}: {start}ms to {end}ms, length: {len(segment)}ms")
                return segments

            segments = split_audio(wav_file_path) if os.path.getsize(wav_file_path) > 25 * 1024 * 1024 else [wav_file_path]

            transcriptions = []
            for i, segment in enumerate(segments):
                transcription_file = os.path.join(transcription_folder, f"transcription_{i}.vtt")

                if os.path.exists(transcription_file):
                    print(f"⏭️ Transcription file {transcription_file} already exists. Skipping this segment.")
                    with open(transcription_file, "r", encoding="utf-8") as file:
                        transcriptions.append(file.read())
                    continue

                custom_prompt_words = []
                custom_prompt = " ".join(custom_prompt_words)

                print(f"✅ Processing {transcription_file}")

                with open(segment, "rb") as audio_file:
                    transcription_response = client.audio.transcriptions.create(
                        model=model_id,
                        file=audio_file,
                        response_format=response_format,
                        prompt=custom_prompt,
                        language="ru"
                    )

                    with open(transcription_file, "w", encoding="utf-8") as file:
                        file.write(transcription_response)

                    transcriptions.append(transcription_response)
            return " ".join(transcriptions)

        except Exception as e:
            print(f" ❌ Failed to transcribe: {e}")
            return None

    return clear_working_directory, convert_to_wav, transcribe_audio_file

# Example usage in main.py
if __name__ == "__main__":
    clear_working_directory, convert_to_wav, transcribe_audio_file = transcribe()

    audio_folder = "./audio"
    for audio_file in os.listdir(audio_folder):
        if audio_file.lower().endswith((".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac")):
            audio_path = os.path.join(audio_folder, audio_file)
            transcription = transcribe_audio_file(audio_path)
