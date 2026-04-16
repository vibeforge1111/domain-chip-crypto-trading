def guard(features: dict, prediction: str) -> str:
    # Filter out trades too close to VWAP (weak signal)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    # Filter out weak momentum trades
    if abs(features.get('macd_histogram', 0)) < 0.0002:
        return "skip"
    return prediction