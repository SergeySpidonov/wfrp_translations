"""
Диагностика: показывает доступные шрифты и создаёт тестовую страницу с текстом.
Запуск: Script → Execute Script в Scribus (без открытых документов).
"""
import scribus

available = sorted(scribus.getFontNames())

# Ищем EB Garamond
eb = [f for f in available if "Garamond" in f or "garamond" in f.lower()]

if eb:
    msg = "Найдены Garamond-шрифты:\n" + "\n".join(eb)
else:
    msg = "EB Garamond НЕ НАЙДЕН!\n\nДругие шрифты (первые 30):\n"
    msg += "\n".join(available[:30])

scribus.messageBox("Доступные шрифты", msg, scribus.ICON_INFORMATION)

# Создаём тестовую страницу
font_to_use = eb[0] if eb else "Times New Roman Regular"

scribus.newDocument(
    (400, 200), (10, 10, 10, 10),
    scribus.PORTRAIT, 1,
    scribus.UNIT_POINTS,
    scribus.PAGE_1, 0, 1
)

tf = scribus.createTextFrame(10, 10, 380, 80, "test1")
scribus.setFont(font_to_use, "test1")
scribus.setFontSize(14, "test1")
scribus.insertText("Тестовый текст / Test text", 0, "test1")
scribus.setFillColor("White", "test1")
scribus.setLineColor("Black", "test1")

scribus.setRedraw(True)
scribus.messageBox("Тест", f"Использован шрифт:\n{font_to_use}\n\nЕсли текст виден на странице — шрифт работает.", scribus.ICON_INFORMATION)
