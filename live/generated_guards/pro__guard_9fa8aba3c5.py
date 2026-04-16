def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value and weak momentum setups."""
    vwap_dev = features.get("vwap_deviation", 0)
    if abs(vwap_dev) < 0.002:
        return "skip"
    rsi_2h = features.get("rsi_2h", 50)
    if rsi_2h > 75 or rsi_2h < 25:
        return "skip"
    return prediction