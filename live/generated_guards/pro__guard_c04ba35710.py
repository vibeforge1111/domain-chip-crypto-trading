def guard(features: dict, prediction: str) -> str:
    # Skip if volume spike without volatility confirmation (liquidity anomaly)
    if features['volume_ratio'] > 1.5 and features['atr_ratio'] < 0.9:
        return "skip"
    # Skip if very small body in high volatility (potential reversal candle)
    if features['body_ratio'] < 0.2 and features['atr_ratio'] > 1.4:
        return "skip"
    return prediction