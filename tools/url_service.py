import urllib.parse


def url_encode(text: str | bytes | bytearray, encoding=None, safety_features=None, parse_plus=False) -> str:
    try:
        encoding = encoding or "utf-8"
        safe = "/"
        if safety_features:
            safe += safety_features

        if isinstance(text, str):
            if parse_plus:
                return urllib.parse.quote_plus(text, encoding=encoding, safe=safe)
            else:
                return urllib.parse.quote(text, encoding=encoding, safe=safe)

        elif isinstance(text, (bytes, bytearray)):
            if parse_plus:
                text_str = text.decode(encoding)
                return urllib.parse.quote_plus(text_str, encoding=encoding, safe=safe)
            else:
                return urllib.parse.quote_from_bytes(text)

        return "❌ Непідтримуваний тип вводу. Введіть строку, байти або байтовий масив."

    except Exception as e:
        return f"❌ Помилка кодування: {str(e)}"


def url_decode(text: str | bytes | bytearray, encoding='utf-8') -> str:
    try:
        if isinstance(text, (bytes, bytearray)):
            text = text.decode(encoding)

        if not isinstance(text, str):
            return "❌ Непідтримуваний тип вводу. Введіть текст, байти або байтовий масив."

        if "+" in text:
            return urllib.parse.unquote_plus(text, encoding=encoding)
        else:
            return urllib.parse.unquote(text, encoding=encoding)

    except Exception as e:
        return f"❌ Помилка декодування: {str(e)}"
