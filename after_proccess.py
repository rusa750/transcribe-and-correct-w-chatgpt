from openai import OpenAI
import os
from dotenv import load_dotenv
from tqdm import tqdm # loading bar


# Load environment variables from a .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set in .env file")


def afterprocess_transcription(txt_folder: str, product_list: list[str]) -> None:
    """
    1) Автоматически обрабатывает все .txt файлы в папке, исправляя ошибки с помощью GPT-4o-mini.
    2) Сохраняет исправленные версии в новые файлы с суффиксом '_corrected'.
    3) Пропускает обработку, если исправленный файл уже существует.

    Args:
        txt_folder (str): Путь к папке с .txt файлами.
        product_list (list[str]): Список названий продуктов и компании, чтобы было легче изменить.

    Returns:
        None
    """
    client = OpenAI()

    system_prompt_template = (
        "Ты — помощник, который исправляет текст расшифровки аудиозаписей на русском языке. "
        "Твоя задача: исправить орфографические ошибки и слова, которые могли быть неправильно распознаны системой. "
        "Особое внимание обрати на следующие названия продуктов: {products}. "
        "Найди их в тексте и исправь их написание при необходимости. "
        "Сохраняй стиль текста и пиши по-русски."
    )

    system_prompt = system_prompt_template.format(products=", ".join(product_list))

    if not os.path.exists(txt_folder):
        print(f"❌ Folder {txt_folder} not found.")
        return

    txt_files = [os.path.join(root, file)
                 for root, _, files in os.walk(txt_folder)
                 for file in files
                 if file.endswith(".txt") and "corrected" not in file.lower()]

    if not txt_files:
        print("⚠️ No files to correct.") # все уже исправлены? Если нет, то есть ошибка
        return

    print(f"- Found {len(txt_files)} files to after-process.")

    # for idx, txt_path in enumerate(txt_files, 1): # old
    for txt_path in tqdm(txt_files, desc="➡️ Correcting", ncols=80):  # <<< adding tqdm
        try:
            corrected_path = txt_path.rsplit(".", 1)[0] + "_corrected.txt"

            if os.path.exists(corrected_path):
                tqdm.write(f"⏭️ Corrected file already exists. Skipping: {corrected_path}")
                continue

            with open(txt_path, "r", encoding="utf-8") as f:
                raw_transcription = f.read()

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": raw_transcription}
                ],
                temperature=0.2,
                max_tokens=4096
            )

            corrected_text = response.choices[0].message.content

            with open(corrected_path, "w", encoding="utf-8") as f:
                f.write(corrected_text)

            tqdm.write(f"✅ Corrected file saved as: {os.path.basename(corrected_path)}")

        except Exception as e:
            tqdm.write(f"❌ Error during correction - {txt_path}: {e}")

# Example usage:
if __name__ == "__main__":
    # Шаг 4: Постобработка всех TXT
    products_to_watch = ["T8 FEEL", "MOBIO+", "T8 BLEND", "T8 STONE", "T8 ViTEN", "T8 Drops", "T8 BEET SHOT", 
                     "T8 TEO GREEN", "NASH Омега-3", "NASH Магний + B6", "NASH ViMi", "NASH PARAKILL", 
                     "NASH Витамин D3", "T8 ERA TO GO Biscuit", "T8 ERA TO GO", "T8 ERA EXO", "T8 EXTRA", 
                     "T8 ERA MIT UP", "Vilavi" ]
    afterprocess_transcription(txt_folder="./transcriptions", product_list=products_to_watch)