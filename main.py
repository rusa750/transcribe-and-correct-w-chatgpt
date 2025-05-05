from convert_video_to_audio import convert_all_videos_to_m4a
from convert_vtt_to_txt import process_vtt_files
from transcribe import transcribe
from after_proccess import afterprocess_transcription
import os

# Шаг 1: Конвертация всех видеофайлов из папки 'video' в .m4a аудио-файлы в папке 'audio'
convert_all_videos_to_m4a()


# Шаг 2.0: Инициализация функций транскрипции (очистка, конвертация в WAV, отправка в Whisper)
clear_working_directory, convert_to_wav, transcribe_audio_file = transcribe()

# Шаг 2.1: Обработка всех аудиофайлов в папке 'audio' — конвертация, нарезка, транскрипция и сохранение в .vtt
audio_folder = "./audio"
for audio_file in os.listdir(audio_folder):
    if audio_file.lower().endswith((".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aac")):
        audio_path = os.path.join(audio_folder, audio_file)
        transcription = transcribe_audio_file(audio_path)
        
# Шаг 3: Преобразование всех .vtt файлов в .txt (удаление тайм-кодов, заголовков, ...)
process_vtt_files()

# Шаг 4: Постобработка .txt файлов — исправление ошибок, стилистики и выделение упоминаний продуктов и компании
products_to_watch = ["T8 FEEL", "MOBIO+", "T8 BLEND", "T8 STONE", "T8 ViTEN", "T8 Drops", "T8 BEET SHOT", 
                     "T8 TEO GREEN", "NASH Омега-3", "NASH Магний + B6", "NASH ViMi", "NASH PARAKILL", 
                     "NASH Витамин D3", "T8 ERA TO GO Biscuit", "T8 ERA TO GO", "T8 ERA EXO", "T8 EXTRA", 
                     "T8 ERA MIT UP", "Vilavi"]
afterprocess_transcription(txt_folder="./transcriptions", product_list=products_to_watch)