import base64
import binascii

def base64_encode(text: str, format: str) -> str:
    try:
        data = text.encode(format.lower())
        encoded = base64.b64encode(data)

        return encoded.decode(format.lower())
   
    except (UnicodeEncodeError, LookupError):
        return f"❌ Encoding failed. Unsupported format: {format}"
