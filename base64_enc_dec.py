import base64
import binascii


def base64_encode(text: str, encoding: str) -> str:
    try:
        data = text.encode(encoding.lower())
        encoded = base64.b64encode(data)

        return encoded.decode(encoding.lower())
   
    except (UnicodeEncodeError, LookupError):
        return f"❌ Encoding failed. Unsupported format: {encoding}"


def base64_decode(text: str, encoding: str) -> str:
    try:
        data = text.encode(encoding.lower())
        decoded = base64.b64decode(data)

        return decoded.decode(encoding.lower())
    
    except (binascii.Error, ValueError):
        return "❌ Base64 decoding failed. Input is not valid base64."
    
    except UnicodeDecodeError:
        return f"❌ Failed to decode bytes to text using '{encoding.lower()}'."
    
    except LookupError:
        return f"❌ Unsupported encoding: {encoding}"