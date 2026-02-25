"""
render_pages.py — рендерит страницы PDF в JPEG для использования как фоны в Scribus.
Использование:
    python scripts/render_pages.py          # все 160 страниц (~120 МБ, ~2-3 мин)
    python scripts/render_pages.py 3 60    # только страницы 3-60
"""
import fitz
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

PDF_PATH   = "Enemy Within Campaign Volume 2 Death on the Reik.pdf"
RENDER_DIR = "renders"
DPI        = 150   # 150 DPI: хорошо для экрана, файлы ~200-400 КБ каждый

os.makedirs(RENDER_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
total = len(doc)

if len(sys.argv) == 3:
    start = int(sys.argv[1]) - 1
    end   = int(sys.argv[2])
else:
    start, end = 0, total

mat = fitz.Matrix(DPI / 72, DPI / 72)

print(f"Рендеринг страниц {start+1}–{end} при {DPI} DPI...")
print(f"Размер страниц: {round(doc[0].rect.width/72*25.4)}×{round(doc[0].rect.height/72*25.4)} мм")

for i in range(start, min(end, total)):
    out_path = os.path.join(RENDER_DIR, f"page{i+1:03d}.jpg")
    if os.path.exists(out_path):
        print(f"  Страница {i+1}: уже есть, пропускаю")
        continue
    pix = doc[i].get_pixmap(matrix=mat, alpha=False)
    with open(out_path, "wb") as f:
        f.write(pix.tobytes("jpg"))
    size_kb = os.path.getsize(out_path) // 1024
    print(f"  Страница {i+1}: {pix.width}×{pix.height}px → {size_kb} КБ")

total_mb = sum(
    os.path.getsize(os.path.join(RENDER_DIR, f))
    for f in os.listdir(RENDER_DIR) if f.endswith(".jpg")
) // (1024 * 1024)
print(f"\nГотово! Папка renders/: {total_mb} МБ")
