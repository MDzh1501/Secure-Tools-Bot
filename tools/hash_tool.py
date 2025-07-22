import hashlib


def hash_text_info(hash_type: str, text: str):
    hash_type = hash_type.lower()

    if hash_type not in hashlib.algorithms_guaranteed:
        return f"❌ Алгоритм \"{hash_type}\" не підтримується"

    encoded = text.encode()

    h = getattr(hashlib, hash_type)()
    h.update(encoded)
    
    return f"🔑 Результат ({hash_type.upper()}):\n`{h.hexdigest()}`"


def hash_file(file_path: str, hash_type: str = "sha256"):
    hash_type = hash_type.lower()

    if hash_type not in hashlib.algorithms_guaranteed:
        return f"❌ Алгоритм \"{hash_type}\" не підтримується."

    try:
        hasher = getattr(hashlib, hash_type)()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return f"🔑 Хеш файлу ({hash_type.upper()}):\n`{hasher.hexdigest()}`"
    except Exception as e:
        return f"❌ Помилка при хешуванні файлу: {str(e)}"


def get_supported_hashes() -> str:
    algos = sorted(hashlib.algorithms_guaranteed)

    formatted = "\n".join(f"• `{algo.upper()}`" for algo in algos)

    return f"🧾 *Доступні алгоритми хешування:*\n\n{formatted}"
