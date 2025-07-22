import base64
import binascii


def base64_encode(text: str, encoding: str) -> str:
    try:
        data = text.encode(encoding.lower())
        encoded = base64.b64encode(data)

        return encoded.decode(encoding.lower())
   
    except (UnicodeEncodeError, LookupError):
        return f"❌ Помилка кодування. Непідтримуваний формат: {encoding}"


def base64_decode(text: str, encoding: str) -> str:
    try:
        data = text.encode(encoding.lower())
        decoded = base64.b64decode(data)

        return decoded.decode(encoding.lower())
    
    except (binascii.Error, ValueError):
        return "❌ Не вдалося декодувати Base64. Вхідні дані не є допустимими для base64."
    
    except UnicodeDecodeError:
        return f"❌ Не вдалося декодувати байти в текст за допомогою '{encoding.lower()}'."
    
    except LookupError:
        return f"❌ Помилка кодування: {encoding}"