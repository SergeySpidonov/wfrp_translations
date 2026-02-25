"""
extract.py — извлечение текста из Death on the Reik по страницам.
Использование:
    python scripts/extract.py              # все страницы
    python scripts/extract.py 5 10        # страницы 5-10 (нумерация с 1)
"""
import fitz
import sys
import os
import json
import re
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PDF_PATH   = "Enemy Within Campaign Volume 2 Death on the Reik.pdf"
OUTPUT_DIR = "translations/death-on-the-reik"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Шрифты-маркеры
SKIP_FONTS    = {"DwarvenAxeBB", "onlyskulls", "CaslonAntique"}
DROPCAP_FONTS = {"CaslonAntique-Bold-SC700"}
HEADER_FONTS  = {"CaslonAntique-Bold"}

def get_span_role(span):
    font = span["font"]
    size = span["size"]
    if font in SKIP_FONTS:
        return "skip"
    if font in DROPCAP_FONTS:
        return "dropcap"   # буквица подзаголовка
    if font in HEADER_FONTS and size >= 14:
        return "h1"
    if "Bold" in font:
        return "bold"
    return "body"

def union_bbox(a, b):
    return [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]

def extract_page(page, page_num):
    raw_blocks = page.get_text("dict")["blocks"]
    result = []

    for block in raw_blocks:
        if block["type"] != 0:
            continue

        block_x0 = block["bbox"][0]
        block_x1 = block["bbox"][2]

        # Собираем items: (role, text, line_bbox)
        # Dropcap-спаны склеиваются в h2 с накоплением bbox строк
        items = []
        dropcap_buf = []
        dropcap_bboxes = []

        for line in block.get("lines", []):
            line_bbox = list(line["bbox"])
            for span in line.get("spans", []):
                role = get_span_role(span)
                text = span["text"]

                if role == "skip":
                    if dropcap_buf:
                        merged = dropcap_bboxes[0]
                        for b in dropcap_bboxes[1:]:
                            merged = union_bbox(merged, b)
                        items.append(("h2", "".join(dropcap_buf).strip(), merged))
                        dropcap_buf = []
                        dropcap_bboxes = []
                    continue

                if role == "dropcap":
                    dropcap_buf.append(text)
                    dropcap_bboxes.append(line_bbox)
                else:
                    if dropcap_buf:
                        merged = dropcap_bboxes[0]
                        for b in dropcap_bboxes[1:]:
                            merged = union_bbox(merged, b)
                        items.append(("h2", "".join(dropcap_buf).strip(), merged))
                        dropcap_buf = []
                        dropcap_bboxes = []
                    items.append((role, text, line_bbox))

        if dropcap_buf:
            merged = dropcap_bboxes[0]
            for b in dropcap_bboxes[1:]:
                merged = union_bbox(merged, b)
            items.append(("h2", "".join(dropcap_buf).strip(), merged))

        if not items:
            continue

        # Группируем последовательные items одного типа,
        # накапливая текст и bbox строк
        groups = []
        cur_type = items[0][0]
        cur_texts = []
        cur_bbox = None

        for role, text, lbbox in items:
            if not text.strip():
                continue
            if role != cur_type and cur_texts:
                groups.append((cur_type, cur_texts, cur_bbox))
                cur_texts = []
                cur_type = role
                cur_bbox = None
            cur_texts.append(text)
            cur_bbox = lbbox if cur_bbox is None else union_bbox(cur_bbox, lbbox)

        if cur_texts:
            groups.append((cur_type, cur_texts, cur_bbox))

        for block_type, texts, bbox in groups:
            combined = " ".join(t for t in texts if t.strip())
            combined = re.sub(r"\s{2,}", " ", combined).strip()
            if not combined:
                continue
            # x — полная ширина колонки из родительского блока,
            # y — только строки данного подблока (не перекрываются)
            final_bbox = [block_x0, bbox[1], block_x1, bbox[3]]
            result.append({
                "type": block_type,
                "text": combined,
                "bbox": final_bbox
            })

    return result

def blocks_to_text(blocks, page_num):
    lines = [f"=== СТРАНИЦА {page_num} ===\n"]
    for b in blocks:
        prefix = {"h1": "[H1] ", "h2": "[H2] ", "bold": "[B] "}.get(b["type"], "")
        lines.append(prefix + b["text"])
        lines.append("")
    return "\n".join(lines)

def main():
    doc = fitz.open(PDF_PATH)
    total = len(doc)

    if len(sys.argv) == 3:
        start, end = int(sys.argv[1]) - 1, int(sys.argv[2])
    else:
        start, end = 0, total

    print(f"Извлекаю страницы {start+1}-{end} из {total}...")

    for i in range(start, min(end, total)):
        page = doc[i]
        blocks = extract_page(page, i + 1)

        if not blocks:
            continue

        txt_path  = os.path.join(OUTPUT_DIR, f"page{i+1:03d}_en.txt")
        json_path = os.path.join(OUTPUT_DIR, f"page{i+1:03d}_blocks.json")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(blocks_to_text(blocks, i + 1))

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(blocks, f, ensure_ascii=False, indent=2)

        print(f"  Страница {i+1}: {len(blocks)} блоков -> {txt_path}")

    print("Готово!")
    print(f"\nДалее: переведи *_en.txt -> *_ru.txt в папке {OUTPUT_DIR}/")
    print("Сохраняй теги [H1], [H2], [B] и пустые строки между блоками.")

if __name__ == "__main__":
    main()
