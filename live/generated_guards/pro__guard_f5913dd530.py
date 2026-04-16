def guard(features: dict, prediction: str) -> str:
    # Skip if weak trend combined with high momentum (likely reversal trap)
    if features['trend_strength'] < 0.3 and features['momentum_score'] > 0.6:
        return "skip"
    # Skip if Bollinger Band squeeze with extreme RSI (volatility expansion likely)
    if features['bb_width'] < 0.5 and (features['rsi_14'] < 30 or features['rsi_14'] > 70):
        return "skip"
    return prediction