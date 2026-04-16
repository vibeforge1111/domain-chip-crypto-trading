def guard(features: dict, prediction: str) -> str:
    # Reject trades when RSI is extreme AND high volume (potential reversal)
    if (features['rsi_14'] > 75 or features['rsi_14'] < 25) and features['volume_ratio'] > 1.4:
        return "skip"
    # Reject when trend is weak but volatility is high (choppy market)
    if features['trend_strength'] < 0.35 and features['volatility_regime'] > 0.65:
        return "skip"
    return prediction