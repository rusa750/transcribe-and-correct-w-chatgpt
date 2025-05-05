import os
import re

def vtt_to_text(vtt_content):
    """Преобразует содержимое файла .vtt в обычный текст, удаляя WEBVTT, временные коды и числа."""
    lines = vtt_content.splitlines()
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.upper() == "WEBVTT":
            continue
        if re.match(r"^\d+$", line):  # skip sequence numbers
            continue
        if re.match(r"\d{2}:\d{2}:\d{2}\.\d{3} -->", line):  # skip timecodes
            continue
        text_lines.append(line)
    return " ".join(text_lines)

def process_vtt_files(base_path="transcriptions", skip_existing=True): #change to True if required to skip
    """
    Обрабатывает все .vtt файлы внутри подпапок указанной директории и сохраняет объединённый текст в .txt файл.

    Для каждой подпапки в `base_path`:
    - Собирает все .vtt файлы.
    - Преобразует их содержимое в обычный текст, удаляя служебные строки и временные коды vtt_to_text().
    - Объединяет результат в один .txt файл с названием, совпадающим с именем папки.
    - Пропускает обработку, если текстовый файл уже существует и `skip_existing=True`.

    Args:
        base_path (str): Путь к root папке, содержащей подпапки с .vtt файлами. По умолчанию "transcriptions".
        skip_existing (bool): Если True, пропускает папки, для которых .txt файл уже существует. По умолчанию True.

    Returns:
        None
    """
    for project_name in os.listdir(base_path):
        project_path = os.path.join(base_path, project_name)
        if os.path.isdir(project_path):
            output_path = os.path.join(project_path, f"{project_name}.txt")
            if skip_existing and os.path.exists(output_path):
                print(f"⏩️ Skipping. '{project_name}' already exists")
                continue

            combined_text = ""
            vtt_files = sorted(
                [f for f in os.listdir(project_path) if f.endswith(".vtt")]
            )
            if not vtt_files:
                print(f"⚠️ No .vtt files found in '{project_name}'")
                continue

            for vtt_file in vtt_files:
                vtt_path = os.path.join(project_path, vtt_file)
                try:
                    with open(vtt_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        plain_text = vtt_to_text(content)
                        combined_text += plain_text + "\n"
                except Exception as e:
                    print(f"❌ Failed to read {vtt_path}: {e}")
                    continue

            try:
                with open(output_path, "w", encoding="utf-8") as out_f:
                    out_f.write(combined_text.strip())
                print(f"✅ Saved: {output_path}")
            except Exception as e:
                print(f"❌ Failed to write output for {project_name}: {e}")

if __name__ == "__main__":
    process_vtt_files()
