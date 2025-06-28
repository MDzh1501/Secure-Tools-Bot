import uuid


def hash_info_uuid(action: str, namespace=None, name=None, hex=None) -> str:
    if action.endswith("1"):
        return str(uuid.uuid1())

    elif action.endswith("2"):
        if not namespace or not name:
            return "❗ uuid3 requires both a namespace and a name."
        return str(uuid.uuid3(namespace, name))

    elif action.endswith("3"):
        return str(uuid.uuid4())

    elif action.endswith("4"):
        if not namespace or not name:
            return "❗ uuid5 requires both a namespace and a name."
        return str(uuid.uuid5(namespace, name))

    elif action.endswith("5"):
        if not hex:
            return "❗ uuid(hex) requires a valid 32-character hex string."
        try:
            return str(uuid.UUID(hex=hex))
        except ValueError:
            return "❌ Invalid hex string for UUID."

    return "❌ Unknown action. Use uuid ending in 1, 2, 3, 4, or 5."