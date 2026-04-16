def guard(features: dict, prediction: str) -> str:
    """Filter trades where candle quality is poor despite strong signals."""
    # Skip if high volatility with weak candle structure (unstable)
    if features['atr_ratio'] > 1.6 and features['body_ratio'] < 0.3:
        return "skip"
    # Skip if momentum diverges from RSI significantly (conflicting signals)
    rsi_normalized = features['rsi_14'] / 100.0
    if abs(features['momentum_score'] - rsi_normalized) > 0.35:
        return "skip"
    return prediction