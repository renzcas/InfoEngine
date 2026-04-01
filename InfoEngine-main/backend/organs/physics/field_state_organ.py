def run(inputs: dict) -> dict:
    state = inputs.get("state", {})
    normalized = {}

    total = sum(abs(float(v)) for v in state.values() if isinstance(v, (int, float)))

    if total == 0:
        return {"field_state": state}

    for k, v in state.items():
        try:
            normalized[k] = float(v) / total
        except:
            normalized[k] = 0

    return {"field_state": normalized}