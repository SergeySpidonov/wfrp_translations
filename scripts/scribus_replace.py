"""
scribus_replace.py — заменяет английский текст русским в импортированном PDF.

Workflow:
  1. File → Import → Import PDF Document
     → выберите PDF → "Импортировать текст как текст" → OK
  2. Script → Execute Script → выберите этот файл
  3. File → Export → Save as PDF
"""
import scribus
import os
import json
import re

WORK_DIR  = r"C:/Users/user/Desktop/ВФРП"
TRANS_DIR = os.path.join(WORK_DIR, "translations", "death-on-the-reik")
TOTAL     = 160

FONT_REG  = "EB Garamond Regular"
FONT_BOLD = "Garamond Bold"
FONT_ITAL = "EB Garamond Italic"

SIZE_MAP = {
    "h1":     (14.0, FONT_BOLD),
    "h2":     (10.0, FONT_BOLD),
    "bold":   (8.0,  FONT_BOLD),
    "italic": (8.0,  FONT_ITAL),
    "body":   (8.0,  FONT_REG),
}


def parse_ru(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    blocks = []
    for raw in re.split(r"\n\s*\n", content.strip()):
        raw = raw.strip()
        if not raw or raw.startswith("=== "):
            continue
        if   raw.startswith("[H1] "): blocks.append(("h1",     raw[5:]))
        elif raw.startswith("[H2] "): blocks.append(("h2",     raw[5:]))
        elif raw.startswith("[B] "):  blocks.append(("bold",   raw[4:]))
        elif raw.startswith("[I] "):  blocks.append(("italic", raw[4:]))
        else:                         blocks.append(("body",   raw))
    return blocks


def get_frame_bbox(name):
    """(x0, y0, x1, y1) фрейма на странице."""
    x, y = scribus.getPosition(name)
    w, h = scribus.getSize(name)
    return (x, y, x + w, y + h)


def overlap_ratio(b1, b2):
    """Доля перекрытия относительно меньшего bbox."""
    ix0 = max(b1[0], b2[0])
    iy0 = max(b1[1], b2[1])
    ix1 = min(b1[2], b2[2])
    iy1 = min(b1[3], b2[3])
    if ix0 >= ix1 or iy0 >= iy1:
        return 0.0
    inter = (ix1 - ix0) * (iy1 - iy0)
    a1 = (b1[2] - b1[0]) * (b1[3] - b1[1])
    a2 = (b2[2] - b2[0]) * (b2[3] - b2[1])
    denom = min(a1, a2)
    return inter / denom if denom > 0 else 0.0


# ── Основной цикл ─────────────────────────────────────────────────────────────

scribus.setRedraw(False)
scribus.progressTotal(TOTAL)

replaced = 0
created  = 0
errors   = []

for page_num in range(1, TOTAL + 1):
    scribus.progressSet(page_num)
    scribus.statusMessage(f"Страница {page_num}/{TOTAL}...")

    ru_path   = os.path.join(TRANS_DIR, f"page{page_num:03d}_ru.txt")
    json_path = os.path.join(TRANS_DIR, f"page{page_num:03d}_blocks.json")

    if not (os.path.exists(ru_path) and os.path.exists(json_path)):
        continue

    ru_blocks = parse_ru(ru_path)
    with open(json_path, encoding="utf-8") as f:
        en_blocks = json.load(f)

    scribus.gotoPage(page_num)

    try:
        items = scribus.getPageItems()
    except Exception as e:
        errors.append(f"p{page_num} getPageItems: {e}")
        continue

    # Текстовые фреймы на странице (тип 4)
    text_frames = [name for name, t, _ in items if t == 4]

    count = min(len(ru_blocks), len(en_blocks))

    for i in range(count):
        btype, ru_text = ru_blocks[i]
        if not ru_text.strip():
            continue

        x0, y0, x1, y1 = en_blocks[i]["bbox"]
        block = (x0, y0, x1, y1)
        w = x1 - x0
        h = y1 - y0
        if w < 1 or h < 1:
            continue

        font_size, font_name = SIZE_MAP.get(btype, SIZE_MAP["body"])
        frame_h = min(h * 1.3, 765.354 - y0 - 2)

        # Ищем все фреймы, перекрывающиеся с нашим блоком
        overlapping = []
        for fname in text_frames:
            try:
                fb = get_frame_bbox(fname)
                ratio = overlap_ratio(block, fb)
                if ratio > 0.2:
                    overlapping.append((ratio, fname))
            except Exception:
                pass

        if not overlapping:
            # Совпадений не найдено — создаём новый фрейм
            try:
                tf = f"ru_{page_num}_{i}"
                scribus.createText(x0, y0, w, frame_h, tf)
                scribus.setFillColor("None", tf)
                scribus.setLineColor("None", tf)
                scribus.setFont(font_name, tf)
                scribus.setFontSize(font_size, tf)
                scribus.insertText(ru_text, 0, tf)
                created += 1
            except Exception as e:
                errors.append(f"p{page_num}[{i}] create: {e}")
            continue

        # Сортируем по степени совпадения
        overlapping.sort(key=lambda x: -x[0])
        best_ratio, best_name = overlapping[0]

        # Удаляем лишние перекрывающиеся фреймы
        for _, fname in overlapping[1:]:
            try:
                scribus.deleteObject(fname)
                text_frames.remove(fname)
            except Exception:
                pass

        # Заменяем текст в лучшем фрейме
        try:
            # Позиционируем и масштабируем под наш блок
            scribus.sizeObject(w, frame_h, best_name)
            scribus.moveObjectAbs(x0, y0, best_name)

            # Очищаем старый текст
            old_text = scribus.getAllText(best_name)
            if old_text:
                scribus.selectText(0, len(old_text), best_name)
                scribus.deleteText(best_name)

            # Вставляем русский текст
            scribus.insertText(ru_text, 0, best_name)
            scribus.selectText(0, len(ru_text), best_name)
            scribus.setFont(font_name, best_name)
            scribus.setFontSize(font_size, best_name)

            replaced += 1
        except Exception as e:
            errors.append(f"p{page_num}[{i}] replace: {e}")

scribus.progressReset()
scribus.setRedraw(True)
scribus.docChanged(True)

# Лог ошибок
LOG_PATH = os.path.join(WORK_DIR, "scribus_errors.txt")
with open(LOG_PATH, "w", encoding="utf-8") as lf:
    lf.write(f"Заменено фреймов: {replaced}\n")
    lf.write(f"Создано новых:    {created}\n")
    lf.write(f"Ошибок:           {len(errors)}\n\n")
    for err in errors[:100]:
        lf.write(err + "\n")

scribus.messageBox(
    "Готово",
    f"Заменено фреймов: {replaced}\n"
    f"Создано новых:    {created}\n"
    f"Ошибок:           {len(errors)}\n\n"
    "Проверьте документ, затем:\n"
    "  File → Export → Save as PDF",
    scribus.ICON_INFORMATION,
)
