import uuid


def hash_info_uuid(action: str, namespace=None, name=None, hex=None) -> str:
    if action.endswith("1"):
        return str(uuid.uuid1())

    elif action.endswith("2"):
        if not namespace or not name:
            return "❗ Такий спосіб uuid вимагає як простір імен, так і ім'я."
        return str(uuid.uuid3(namespace, name))

    elif action.endswith("3"):
        return str(uuid.uuid4())

    elif action.endswith("4"):
        if not namespace or not name:
            return "❗ Такий спосіб uuid вимагає як простір імен, так і ім'я."
        return str(uuid.uuid5(namespace, name))

    elif action.endswith("5"):
        if not hex:
            return "❗ Такий спосіб uuid вимагає дійсного 32-символьного шістнадцяткового рядка."
        try:
            return str(uuid.UUID(hex=hex))
        except ValueError:
            return "❌ Неправильний шістнадцятковий рядок для UUID."

    return "❌ Невідома дія. Використовуйте uuid, що закінчується на 1, 2, 3, 4 або 5."