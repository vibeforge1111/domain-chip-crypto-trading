def guard(features: dict, prediction: str) -> str:
    """Reject trades when price is overextended at BB extremes with extreme RSI."""
    rsi = features.get("rsi_14", 50)
    bb_pos = features.get("bb_position", 0.5)
    if prediction == "long" and rsi > 70 and bb_pos > 0.85:
        return "skip"
    if prediction == "short" and rsi < 30 and bb_pos < 0.15:
        return "skip"
    return prediction