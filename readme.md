# Audio Transcription Pipeline with GPT Postprocessing

This project provides an automated pipeline for:
- Converting videos to audio (.m4a)
- Transcribing audio using OpenAI Whisper API
- Converting .vtt files to plain .txt
- Postprocessing text using GPT for grammar and semantic cleanup

---

## Project Structure

```
project-root/
├── audio/                 # Automatically created - stores extracted audio files
├── video/                 # Input video files
├── transcriptions/        # Output directories with transcription and text files
├── working/               # Temporary WAV segments for Whisper API
├── .env                   # Contains OPENAI_API_KEY
├── main.py                # Entry point script
├── transcribe.py          # Transcription module with segment splitting
├── convert_video_to_audio.py
├── convert_vtt_to_txt.py
├── after_proccess.py
```

---

## Requirements

Install required dependencies:

```bash
pip install -r requirements.txt
```

Content of `requirements.txt`:

```
openai
pydub
python-dotenv
```

You also need to have [ffmpeg](https://ffmpeg.org/download.html) installed in your system for `pydub` to work.

---

## API Key Configuration

Create a `.env` file in the root directory with the following content:

```
OPENAI_API_KEY=sk-...
```

---

## Usage

Run the full pipeline:

```bash
python main.py
```

`main.py` does the following:

1. Converts all video files in `video/` folder to `.m4a` format in the `audio/` folder.
2. Transcribes all supported audio files using Whisper API. If audio is over 25MB, it is split into segments.
3. Converts all `.vtt` transcription files into cleaned `.txt` files.
4. Postprocesses all `.txt` files to improve grammar and extract key product mentions.

---

## Supported Formats

Video:
- .mp4, .mov, .avi, .mkv, .webm

Audio:
- .wav, .mp3, .ogg, .flac, .m4a, .aac

---

## Configuration

You can define a list of products to track in the `main.py` script like this:

```python
products_to_watch = ["T8 FEEL", "MOBIO+", "T8 BLEND", "NASH Омега-3", "Vilavi", ...]
afterprocess_transcription(txt_folder="./transcriptions", product_list=products_to_watch)
```

