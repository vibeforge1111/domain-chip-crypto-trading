def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum and RSI diverge (potential reversal)."""
    # Long when RSI elevated but EMA flat/downward (momentum divergence)
    if prediction == "long" and features['rsi_14'] > 65 and features['ema_slope'] < 0:
        return "skip"
    # Short when RSI low but EMA upward (potential bounce setup)
    if prediction == "short" and features['rsi_14'] < 40 and features['ema_slope'] > 0:
        return "skip"
    return prediction