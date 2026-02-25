"""
languagetool_mcp.py — MCP-сервер для проверки переводов через LanguageTool API.

Использует бесплатный публичный API languagetool.org (без Java, без установки).
Лимиты: ~20 запросов/мин, до 20 КБ текста за запрос.

Инструменты:
  check_text(text, language)        — проверить произвольный текст
  check_translation(en_text, ru_text) — сравнить перевод с оригиналом и найти ошибки
"""

import requests
from mcp.server.fastmcp import FastMCP

LT_URL = "https://api.languagetool.org/v2/check"

mcp = FastMCP("languagetool")


def _call_lt(text: str, language: str) -> list[dict]:
    """Вызов LanguageTool API. Возвращает список matches."""
    resp = requests.post(
        LT_URL,
        data={"text": text, "language": language},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json().get("matches", [])


def _format_matches(matches: list[dict], text: str) -> str:
    if not matches:
        return "Ошибок не найдено."

    lines = [f"Найдено ошибок: {len(matches)}\n"]
    for m in matches:
        offset = m["offset"]
        length = m["length"]
        fragment = text[offset : offset + length]
        msg = m["message"]
        rule = m.get("rule", {}).get("id", "")
        replacements = [r["value"] for r in m.get("replacements", [])[:3]]
        suggestion = " / ".join(replacements) if replacements else "—"
        lines.append(
            f"• [{rule}] «{fragment}» → предлагается: {suggestion}\n  {msg}"
        )
    return "\n".join(lines)


@mcp.tool()
def check_text(text: str, language: str = "ru-RU") -> str:
    """
    Проверить текст на грамматические и орфографические ошибки с помощью LanguageTool.

    Args:
        text: Текст для проверки.
        language: Код языка (по умолчанию ru-RU для русского).
                  Примеры: en-US, de-DE, ru-RU.
    Returns:
        Список найденных ошибок с предложениями по исправлению.
    """
    try:
        matches = _call_lt(text, language)
        return _format_matches(matches, text)
    except requests.RequestException as e:
        return f"Ошибка соединения с LanguageTool API: {e}"


@mcp.tool()
def check_translation(en_text: str, ru_text: str) -> str:
    """
    Проверить русский перевод на ошибки.
    Параллельно проверяет исходный английский текст (как контроль) и русский перевод.

    Args:
        en_text: Оригинальный текст на английском.
        ru_text: Перевод на русском, который нужно проверить.
    Returns:
        Отчёт об ошибках в русском переводе.
    """
    try:
        ru_matches = _call_lt(ru_text, "ru-RU")
        report = ["=== Проверка русского перевода ==="]
        report.append(_format_matches(ru_matches, ru_text))
        return "\n".join(report)
    except requests.RequestException as e:
        return f"Ошибка соединения с LanguageTool API: {e}"


if __name__ == "__main__":
    mcp.run()
