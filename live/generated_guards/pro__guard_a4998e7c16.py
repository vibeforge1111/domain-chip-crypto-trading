def guard(features: dict, prediction: str) -> str:
    # Filter trades too close to fair value (VWAP)
    vwap_dev = features.get('vwap_deviation', 0)
    if abs(vwap_dev) < 0.004:
        return "skip"
    # Additional filter: skip if conflicting with longer-term RSI context
    rsi_2h = features.get('rsi_2h', 50)
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    return prediction