import os
import subprocess

def convert_all_videos_to_m4a():
    """
    1) Конвертирует все видеофайлы из папки 'video' в аудиофайлы формата .m4a и сохраняет их в папку 'audio'.

    2) Использует утилиту ffmpeg для извлечения аудио-дорожек из файлов форматов .mp4, .mov, .avi, .mkv, .webm.
    3) Пропускает видеофайлы, если соответствующий .m4a-файл уже существует.
    4) Название создаваемого файла имеет суффикс ' - from video.m4a'.

    5) Папка 'audio' создаётся автоматически, если её нет.

    Returns:
        None
    """
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.join(root_dir, "video")
    audio_dir = os.path.join(root_dir, "audio")

    # Create audio folder if it doesn't exist
    os.makedirs(audio_dir, exist_ok=True)

    # List all files in the video folder
    for filename in os.listdir(video_dir):
        if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
            video_path = os.path.join(video_dir, filename)
            name_without_ext = os.path.splitext(filename)[0]
            audio_filename = f"{name_without_ext} - from video.m4a"
            audio_path = os.path.join(audio_dir, audio_filename)
            
            # Skip if the target audio file already exists
            if os.path.exists(audio_path):
                print(f"⏭️ Audio already exist. Skipping: {audio_filename}")
                continue

            print(f"Converting: {filename} → {audio_filename}")

            try:
                subprocess.run([
                    "ffmpeg",
                    "-i", video_path,
                    "-vn",
                    "-acodec", "aac",
                    "-b:a", "192k",
                    audio_path
                ], check=True)
                print(f"✅ Saved to: {audio_path}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to convert {filename}: {e}")

if __name__ == "__main__":
    convert_all_videos_to_m4a()
