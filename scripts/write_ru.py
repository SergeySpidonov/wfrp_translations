"""
apply.py — вставляет переведённый текст в PDF.
Использование:
    python scripts/apply.py              # все переведённые страницы
    python scripts/apply.py 5 10        # страницы 5-10
"""
import fitz
import sys
import os
import json
import re
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PDF_PATH      = "Enemy Within Campaign Volume 2 Death on the Reik.pdf"
OUTPUT_PATH   = "Смерть на Рейке (v1-0).pdf"
TRANS_DIR     = "translations"

# Файлы шрифтов с кириллицей (Windows)
FONT_FILES = {
    "body":   "C:/Windows/Fonts/times.ttf",
    "bold":   "C:/Windows/Fonts/timesbd.ttf",
    "italic": "C:/Windows/Fonts/timesi.ttf",
    "bolditalic": "C:/Windows/Fonts/timesbi.ttf",
}

# Соответствие типа блока → (размер, ключ шрифта)
# Чуть уменьшаем, потому что русский текст длиннее
SIZE_MAP = {
    "h1":     (15.0, "bold"),
    "h2":     (10.5, "bold"),
    "bold":   (8.5,  "bold"),
    "italic": (8.5,  "italic"),
    "body":   (8.5,  "body"),
}

def parse_translation(filepath):
    """Читает *_ru.txt и возвращает список блоков [{type, text}]"""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    blocks = []
    raw_blocks = re.split(r"\n\s*\n", content.strip())

    for raw in raw_blocks:
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("=== "):
            continue  # заголовок файла, пропускаем

        if raw.startswith("[H1] "):
            blocks.append({"type": "h1", "text": raw[5:]})
        elif raw.startswith("[H2] "):
            blocks.append({"type": "h2", "text": raw[5:]})
        elif raw.startswith("[B] "):
            blocks.append({"type": "bold", "text": raw[4:]})
        elif raw.startswith("[I] "):
            blocks.append({"type": "italic", "text": raw[4:]})
        else:
            blocks.append({"type": "body", "text": raw})

    return blocks

def apply_page(page, en_blocks, ru_blocks):
    """Затирает оригинальный текст и вставляет перевод."""

    if len(ru_blocks) != len(en_blocks):
        print(f"  ВНИМАНИЕ: количество блоков не совпадает "
              f"(EN: {len(en_blocks)}, RU: {len(ru_blocks)}). "
              f"Применяю по минимуму.")

    count = min(len(en_blocks), len(ru_blocks))

    for i in range(count):
        en_block = en_blocks[i]
        ru_block = ru_blocks[i]

        bbox = fitz.Rect(en_block["bbox"])
        block_type = ru_block["type"]
        text = ru_block["text"]
        font_size, font_key = SIZE_MAP.get(block_type, SIZE_MAP["body"])
        font_file = FONT_FILES[font_key]
        # Уникальное имя шрифта на странице, чтобы избежать конфликтов
        font_alias = f"F_{font_key}"

        # 1. Закрашиваем оригинальный блок белым прямоугольником
        page.draw_rect(bbox, color=(1, 1, 1), fill=(1, 1, 1))

        # 2. Вставляем русский текст с явным файлом шрифта
        def try_insert(size):
            return page.insert_textbox(
                bbox,
                text,
                fontsize=size,
                fontfile=font_file,
                fontname=font_alias,
                color=(0, 0, 0),
                align=0
            )

        try:
            rc = try_insert(font_size)
            if rc < 0:
                # Текст не влез — уменьшаем шрифт
                try_insert(font_size * 0.82)
        except Exception as e:
            print(f"    Ошибка вставки блока {i}: {e}")

def main():
    doc = fitz.open(PDF_PATH)
    total = len(doc)

    if len(sys.argv) == 3:
        start, end = int(sys.argv[1]) - 1, int(sys.argv[2])
    else:
        start, end = 0, total

    modified = 0

    for i in range(start, min(end, total)):
        ru_path    = os.path.join(TRANS_DIR, f"page{i+1:03d}_ru.txt")
        json_path  = os.path.join(TRANS_DIR, f"page{i+1:03d}_blocks.json")

        if not os.path.exists(ru_path):
            continue  # страница ещё не переведена
        if not os.path.exists(json_path):
            print(f"  Нет JSON для страницы {i+1}, пропускаю")
            continue

        with open(json_path, encoding="utf-8") as f:
            en_blocks = json.load(f)

        ru_blocks = parse_translation(ru_path)

        if not ru_blocks:
            continue

        page = doc[i]
        apply_page(page, en_blocks, ru_blocks)
        modified += 1
        print(f"  Страница {i+1}: {len(ru_blocks)} блоков вставлено")

    if modified == 0:
        print("Нет переведённых страниц. Сначала запусти extract.py и переведи файлы.")
        return

    doc.save(OUTPUT_PATH, garbage=4, deflate=True)
    print(f"\nГотово! Сохранено: {OUTPUT_PATH} ({modified} страниц обработано)")

if __name__ == "__main__":
    main()
