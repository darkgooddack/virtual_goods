import uuid


def generate_idempotency_key(user_id: str, product_id: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{user_id}:{product_id}"))
