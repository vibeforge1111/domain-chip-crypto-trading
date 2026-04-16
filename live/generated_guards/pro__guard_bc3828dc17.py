def guard(features: dict, prediction: str) -> str:
    """Reject trades where candle structure contradicts the predicted direction."""
    if prediction == "long":
        # Long with dominant upper wick and bearish EMA = rejection candidate
        if features["upper_wick_ratio"] > 0.4 and features["ema_slope"] < -0.1:
            return "skip"
    elif prediction == "short":
        # Short with dominant lower wick and bullish EMA = rejection candidate
        if features["lower_wick_ratio"] > 0.4 and features["ema_slope"] > 0.1:
            return "skip"
    return prediction