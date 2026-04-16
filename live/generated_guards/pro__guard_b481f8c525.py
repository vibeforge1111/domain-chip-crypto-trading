def guard(features: dict, prediction: str) -> str:
    # Skip trades too close to fair value (VWAP)
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.001:
        return "skip"
    # Additional filter: reject extremes with weak momentum alignment
    stoch_k = features.get('stoch_k', 50)
    macd = features.get('macd_histogram', 0)
    if (stoch_k > 85 and macd < 0) or (stoch_k < 15 and macd > 0):
        return "skip"
    return prediction