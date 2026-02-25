"""
generate_sla.py — создаёт Scribus-документ (.sla) с оригинальными страницами
как фоном и русским текстом поверх переведённых блоков.

Использование:
    python scripts/generate_sla.py

Результат: Смерть_на_Рейке.sla  — открыть в Scribus, скорректировать шрифты,
           экспортировать в PDF (File → Export → Save as PDF).

Требования:
    - Папка renders/ с JPEG-рендерами страниц (python scripts/render_pages.py)
    - Папка translations/ с *_ru.txt и *_blocks.json
    - В Scribus установлен шрифт EB Garamond (или изменить FONT_* ниже)
"""

import os
import sys
import json
import re
from xml.etree.ElementTree import Element, SubElement, ElementTree

sys.stdout.reconfigure(encoding="utf-8")

# ── Пути ──────────────────────────────────────────────────────────────────────
RENDER_DIR  = "renders"
TRANS_DIR   = "translations"
OUTPUT_SLA  = "Смерть_на_Рейке.sla"

# ── Размер страницы (в пунктах, из оригинального PDF) ─────────────────────────
PAGE_W      = 609.449   # 215 мм
PAGE_H      = 765.354   # 270 мм
TOTAL_PAGES = 160

# ── Шрифты ────────────────────────────────────────────────────────────────────
FONT_REGULAR = "EB Garamond Regular"
FONT_BOLD    = "EB Garamond SemiBold"
FONT_ITALIC  = "EB Garamond Italic"

# ── Карта размеров и стилей ───────────────────────────────────────────────────
SIZE_MAP = {
    "h1":     (14.0, FONT_BOLD,    "H1Color"),
    "h2":     (10.0, FONT_BOLD,    "H2Color"),
    "bold":   (8.0,  FONT_BOLD,    "Black"),
    "italic": (8.0,  FONT_ITALIC,  "Black"),
    "body":   (8.0,  FONT_REGULAR, "Black"),
}

FRAME_H_EXPAND = 0.25   # +25% к высоте фрейма (русский текст длиннее)


# ── Вспомогательные функции ───────────────────────────────────────────────────

def parse_ru_blocks(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()
    blocks = []
    for raw in re.split(r"\n\s*\n", content.strip()):
        raw = raw.strip()
        if not raw or raw.startswith("=== "):
            continue
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


def s(v):
    """Конвертирует значение в строку для XML-атрибута."""
    return str(v)


# ── Сборка документа ─────────────────────────────────────────────────────────

def build_sla():
    root = Element("SCRIBUSUTF8NEW")
    root.set("Version", "1.5.8")

    # ── DOCUMENT ──────────────────────────────────────────────────────────────
    doc = SubElement(root, "DOCUMENT")
    doc.attrib.update({
        "ANZPAGES":    s(TOTAL_PAGES),
        "PAGEWIDTH":   "609.449",
        "PAGEHEIGHT":  "765.354",
        "BORDERLEFT":  "0", "BORDERRIGHT": "0",
        "BORDERTOP":   "0", "BORDERBOTTOM": "0",
        "ORIENTATION": "0",
        "PAGETYPE":    "0",
        "FIRSTNUM":    "1",
        "NUMPAGES":    "0",
        "DOCDATE":     "", "DOCAUTHORS": "", "DOCTITLE": "",
        "UNITS":       "0",      # ← UNITS, не UNIT
        "AUTOWIDTH":   "0",
        "SPREAD":      "0",
        "PAGESIZE":    "Custom",
        "FIRSTLEFT":   "0",
        "DPPIX":       "72", "DPPIY": "72",
        "VHOCH":       "33", "VHOCHSC": "100",
        "VTIEF":       "33", "VTIEFSC": "100",
        "KURSIV":      "1",  "SKAPITAL": "75",
        "BASEGRID":    "14.4", "BASEO": "0",
        "AUTOSAVE":    "0", "AUTOSAVETIME": "600",
        "COMPRESS":    "1", "SAVECOMPRESSED": "0",
    })

    # ── Цвета ─────────────────────────────────────────────────────────────────
    for name, space, vals in [
        ("Black",   "CMYK", {"C": "0",  "M": "0",   "Y": "0",   "K": "100"}),
        ("None",    "CMYK", {"C": "0",  "M": "0",   "Y": "0",   "K": "0", "REGISTER": "1"}),
        ("White",   "CMYK", {"C": "0",  "M": "0",   "Y": "0",   "K": "0"}),
        ("H1Color", "RGB",  {"R": "74", "G": "0",   "B": "0"}),
        ("H2Color", "RGB",  {"R": "44", "G": "44",  "B": "110"}),
    ]:
        c = SubElement(doc, "COLOR")
        c.set("NAME", name)
        c.set("SPACE", space)
        c.attrib.update(vals)

    # ── Стиль абзаца ──────────────────────────────────────────────────────────
    style = SubElement(doc, "STYLE")
    style.attrib.update({
        "NAME":            "Default Paragraph Style",
        "PARENT":          "",
        "LINESPACINGMODE": "1",
        "LINESPACING":     "12",
        "FONT":            FONT_REGULAR,
        "FONTSIZE":        "8",
        "ALIGN":           "0",
    })

    # ── LAYERS — обязательный раздел ──────────────────────────────────────────
    layer = SubElement(doc, "LAYERS")
    layer.attrib.update({
        "LEVEL":     "0",
        "TYPE":      "0",
        "VISIBLE":   "1",
        "PRINTABLE": "1",
        "LOCKED":    "0",
        "FLOW":      "1",
        "TRANS":     "1",
        "BLEND":     "0",
        "NAME":      "Background",
        "NUMMER":    "0",
    })

    # ── Мастер-страница ───────────────────────────────────────────────────────
    mp = SubElement(doc, "MASTERPAGE")
    mp.attrib.update({
        "NAME":         "Normal", "PAGENAME": "Normal",
        "PAGEWIDTH":    "609.449", "PAGEHEIGHT": "765.354",
        "BORDERLEFT":   "0", "BORDERRIGHT": "0",
        "BORDERTOP":    "0", "BORDERBOTTOM": "0",
        "ORIENTATION":  "0", "PAGETYPE": "0",
        "PAGESIZE":     "Custom", "FIRSTNUM": "0",
    })

    # ── Sections — нумерация страниц ──────────────────────────────────────────
    sections = SubElement(doc, "Sections")
    sec = SubElement(sections, "Section")
    sec.attrib.update({
        "Name":       "",
        "Active":     "1",
        "From":       "0",
        "To":         s(TOTAL_PAGES - 1),
        "Type":       "Type_1_2_3",
        "Start":      "1",
        "Reversed":   "0",
        "ShowPages":  "1",
    })

    # ── Собираем данные о страницах ───────────────────────────────────────────
    pages_data = []   # [{img_path, blocks: [{type,text,bbox}]}]

    for page_num in range(1, TOTAL_PAGES + 1):
        img_abs = os.path.abspath(os.path.join(RENDER_DIR, f"page{page_num:03d}.jpg"))
        img_path = f"renders/page{page_num:03d}.jpg" if os.path.exists(img_abs) else None

        ru_path   = os.path.join(TRANS_DIR, f"page{page_num:03d}_ru.txt")
        json_path = os.path.join(TRANS_DIR, f"page{page_num:03d}_blocks.json")

        blocks = []
        if os.path.exists(ru_path) and os.path.exists(json_path):
            ru_blocks = parse_ru_blocks(ru_path)
            with open(json_path, encoding="utf-8") as f:
                en_blocks = json.load(f)
            count = min(len(ru_blocks), len(en_blocks))
            for i in range(count):
                if ru_blocks[i]["text"].strip():
                    blocks.append({
                        "type": ru_blocks[i]["type"],
                        "text": ru_blocks[i]["text"],
                        "bbox": en_blocks[i]["bbox"],
                    })

        pages_data.append({"img_path": img_path, "blocks": blocks})

    # ── 1. Все PAGE элементы ──────────────────────────────────────────────────
    for page_idx, _ in enumerate(pages_data):
        y_pos = page_idx * PAGE_H
        page_el = SubElement(doc, "PAGE")
        page_el.attrib.update({
            "PAGENAME":    "",
            "NUM":         s(page_idx),
            "PAGEXPOS":    "0",
            "PAGEYPOS":    f"{y_pos:.3f}",
            "PAGEWIDTH":   "609.449",
            "PAGEHEIGHT":  "765.354",
            "BORDERLEFT":  "0", "BORDERRIGHT": "0",
            "BORDERTOP":   "0", "BORDERBOTTOM": "0",
            "ORIENTATION": "0", "PAGETYPE": "0",
            "PAGESIZE":    "Custom",
            "MASTERPAGE":  "Normal",
            "FIRSTNUM":    "0",
            "NUMERATION":  "0",
            "NUMPAGES":    "0",
        })

    # ── 2. Все PAGEOBJECT элементы ────────────────────────────────────────────
    translated_count = 0

    for page_idx, pdata in enumerate(pages_data):
        y_off = page_idx * PAGE_H

        # Фоновое изображение
        if pdata["img_path"]:
            obj = SubElement(doc, "PAGEOBJECT")
            obj.attrib.update({
                "XPOS": "0", "YPOS": f"{y_off:.3f}",
                "WIDTH": "609.449", "HEIGHT": "765.354",
                "OwnPage":     s(page_idx),
                "PTYPE":       "2",
                "PFILE":       pdata["img_path"],
                "SCALETYPE":   "0",
                "RATIO":       "1",
                "LOCALSCX":    "1", "LOCALSCY": "1",
                "LOCALX":      "0", "LOCALY": "0",
                "PICART":      "1",
                "FILLCOLOR":   "None", "FILLSHADE": "100",
                "LINECOLOR":   "None", "LINEWIDTH": "0",
                "PRINTOBJECT": "1",
                "LAYER":       "0",
                "NEXTIT":      "-1", "BACKITEM": "-1",
                "ANNAME":      f"bg_{page_idx+1:03d}",
            })

        # Текстовые фреймы
        if pdata["blocks"]:
            translated_count += 1
            for b in pdata["blocks"]:
                x0, y0, x1, y1 = b["bbox"]
                w = x1 - x0
                h = min((y1 - y0) * (1 + FRAME_H_EXPAND), PAGE_H - y0 - 1)
                font_size, font_name, text_color = SIZE_MAP.get(b["type"], SIZE_MAP["body"])

                obj = SubElement(doc, "PAGEOBJECT")
                obj.attrib.update({
                    "XPOS":        f"{x0:.3f}",
                    "YPOS":        f"{y_off + y0:.3f}",
                    "WIDTH":       f"{w:.3f}",
                    "HEIGHT":      f"{h:.3f}",
                    "OwnPage":     s(page_idx),
                    "PTYPE":       "4",
                    "FILLCOLOR":   "None", "FILLSHADE": "100",
                    "LINECOLOR":   "None", "LINEWIDTH": "0",
                    "PRINTOBJECT": "1",
                    "LAYER":       "0",
                    "COLUMNS":     "1", "COLGAP": "0",
                    "AUTOTEXT":    "0",
                    "NEXTIT":      "-1", "BACKITEM": "-1",
                    "LANGUAGE":    "ru",
                    "ANNAME":      f"txt_{page_idx+1:03d}_{int(x0)}_{int(y0)}",
                })

                story = SubElement(obj, "StoryText")
                itext = SubElement(story, "ITEXT")
                itext.attrib.update({
                    "FONT":     font_name,
                    "FONTSIZE": f"{font_size:.1f}",
                    "FCOLOR":   text_color,
                    "CH":       b["text"],
                })
                para = SubElement(story, "para")
                para.set("PARENT", "Default Paragraph Style")

        page_num = page_idx + 1
        if pdata["blocks"]:
            print(f"  Страница {page_num}: {len(pdata['blocks'])} фреймов")

    print(f"\nВсего переведённых страниц: {translated_count}")
    return root


def main():
    print("Генерация Scribus SLA...")
    root = build_sla()

    # Записываем XML с отступами
    _indent(root)
    tree = ElementTree(root)

    with open(OUTPUT_SLA, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="utf-8", xml_declaration=False)

    size_mb = os.path.getsize(OUTPUT_SLA) / (1024 * 1024)
    print(f"\nГотово! → {OUTPUT_SLA} ({size_mb:.1f} МБ)")
    print("\nСледующий шаг: откройте файл в Scribus")
    print("  Extra → Manage Fonts → убедитесь, что EB Garamond есть в списке")
    print("  File → Export → Save as PDF")


def _indent(elem, level=0):
    pad = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = pad + "  "
        for child in elem:
            _indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = pad
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = pad


if __name__ == "__main__":
    main()
