def run(inputs: dict) -> dict:
    state = inputs.get("state", {})
    energy = 0.0

    for _, v in state.items():
        try:
            energy += float(v) ** 2
        except (TypeError, ValueError):
            continue

    return {"energy": energy}