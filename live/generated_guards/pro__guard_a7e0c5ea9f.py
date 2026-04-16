def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak volume confirmation or conflicting signals."""
    # Filter if volume doesn't confirm the move
    if features["volume_ratio"] < 0.7:
        return "skip"
    # Filter if EMA slope contradicts prediction direction
    if prediction == "long" and features["ema_slope"] < 0:
        return "skip"
    if prediction == "short" and features["ema_slope"] > 0:
        return "skip"
    # Filter if RSI overbought/oversold contradicts direction
    if prediction == "long" and features["rsi_14"] < 40:
        return "skip"
    if prediction == "short" and features["rsi_14"] > 60:
        return "skip"
    # Filter if strong trend but low momentum alignment
    if features["trend_strength"] > 0.7 and features["momentum_score"] < 30:
        return "skip"
    return prediction