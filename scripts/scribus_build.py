"""
scribus_build.py — строит переведённый документ через Scribus Python API.

Запуск:
  1. Откройте Scribus (без документов)
  2. Script → Execute Script → выберите этот файл
  3. Дождитесь завершения (~3-5 минут)
  4. File → Export → Save as PDF
"""
import scribus
import os
import json
import re

# ── Пути ──────────────────────────────────────────────────────────────────────
WORK_DIR   = r"C:/Users/user/Desktop/ВФРП"
PDF_PATH   = os.path.join(WORK_DIR, "Enemy Within Campaign Volume 2 Death on the Reik.pdf")
RENDER_DIR = os.path.join(WORK_DIR, "renders")
TRANS_DIR  = os.path.join(WORK_DIR, "translations", "death-on-the-reik")

PAGE_W = 609.449
PAGE_H = 765.354
TOTAL  = 160

# ── Шрифты (точные названия из Scribus) ──────────────────────────────────────
FONT_REG  = "EB Garamond Regular"
FONT_BOLD = "Garamond Bold"       # EB Garamond Bold не установлен, берём Garamond Bold
FONT_ITAL = "EB Garamond Italic"

SIZE_MAP = {
    "h1":     (14.0, FONT_BOLD),
    "h2":     (10.0, FONT_BOLD),
    "bold":   (8.0,  FONT_BOLD),
    "italic": (8.0,  FONT_ITAL),
    "body":   (8.0,  FONT_REG),
}

# ── Вспомогательные функции ───────────────────────────────────────────────────

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


# ── Основной код ─────────────────────────────────────────────────────────────

scribus.statusMessage(f"Шрифты: {FONT_REG} / {FONT_BOLD}")
scribus.setRedraw(False)

# Создаём документ: 160 страниц, размер в пунктах, нулевые поля
scribus.newDocument(
    (PAGE_W, PAGE_H),   # ширина × высота в пунктах
    (0, 0, 0, 0),       # поля: верх, лево, право, низ
    scribus.PORTRAIT,
    1,                  # первый номер страницы
    scribus.UNIT_POINTS,
    scribus.PAGE_1,     # одна страница (не разворот)
    0,
    TOTAL,
)

scribus.progressTotal(TOTAL)
text_frames_created = 0
errors = []

for page_num in range(1, TOTAL + 1):
    scribus.progressSet(page_num)
    scribus.statusMessage(f"Страница {page_num}/{TOTAL}...")
    scribus.gotoPage(page_num)

    # ── Фоновое изображение (JPEG-рендер) ────────────────────────────────────
    img_path = os.path.join(RENDER_DIR, f"page{page_num:03d}.jpg")
    bg_name  = f"bg_{page_num:03d}"
    bg = scribus.createImage(0, 0, PAGE_W, PAGE_H, bg_name)
    scribus.setLineColor("None", bg_name)
    if os.path.exists(img_path):
        scribus.loadImage(img_path, bg_name)
        scribus.setScaleImageToFrame(True, True, bg_name)
    scribus.lockObject(bg_name)  # фон заблокирован — не мешает выделять текст

    # ── Текстовые фреймы ─────────────────────────────────────────────────────
    ru_path   = os.path.join(TRANS_DIR, f"page{page_num:03d}_ru.txt")
    json_path = os.path.join(TRANS_DIR, f"page{page_num:03d}_blocks.json")

    if not (os.path.exists(ru_path) and os.path.exists(json_path)):
        continue

    ru_blocks = parse_ru(ru_path)
    with open(json_path, encoding="utf-8") as f:
        en_blocks = json.load(f)

    for i in range(min(len(ru_blocks), len(en_blocks))):
        btype, text = ru_blocks[i]
        if not text.strip():
            continue

        x0, y0, x1, y1 = en_blocks[i]["bbox"]
        w = x1 - x0
        h = min((y1 - y0) * 1.3, PAGE_H - y0 - 2)
        if w < 1 or h < 1:
            continue

        font_size, font_name = SIZE_MAP.get(btype, SIZE_MAP["body"])
        tf_name = f"t{page_num}_{i}"

        try:
            # Белый прямоугольник закрывает английский текст на фоне
            rect_name = f"r{page_num}_{i}"
            scribus.createRect(x0, y0, w, h, rect_name)
            scribus.setFillColor("White", rect_name)
            scribus.setLineColor("None", rect_name)
            scribus.lockObject(rect_name)  # белый прямоугольник заблокирован
            # Русский текст поверх белого прямоугольника
            scribus.createText(x0, y0, w, h, tf_name)
            scribus.setFillColor("None", tf_name)
            scribus.setLineColor("None", tf_name)
            scribus.setFont(font_name, tf_name)
            scribus.setFontSize(font_size, tf_name)
            scribus.insertText(text, 0, tf_name)
            text_frames_created += 1
        except Exception as e:
            errors.append(f"p{page_num}[{i}] {btype}: {e}")

scribus.progressReset()
scribus.setRedraw(True)
scribus.docChanged(True)

# Записываем лог ошибок
LOG_PATH = os.path.join(WORK_DIR, "scribus_errors.txt")
with open(LOG_PATH, "w", encoding="utf-8") as lf:
    lf.write(f"Фреймов создано: {text_frames_created}\n")
    lf.write(f"Ошибок: {len(errors)}\n\n")
    for err in errors[:50]:   # первые 50
        lf.write(err + "\n")

scribus.statusMessage("Готово! Сохраните файл: File → Save as, затем File → Export → Save as PDF")

scribus.messageBox(
    "Готово",
    f"Документ построен: {TOTAL} страниц.\n"
    f"Текстовых фреймов создано: {text_frames_created}\n"
    f"Шрифт: {FONT_REG}\n\n"
    "Теперь:\n"
    "  File → Save As → Смерть_на_Рейке_v2.sla\n"
    "  File → Export → Save as PDF",
    scribus.ICON_INFORMATION,
)
