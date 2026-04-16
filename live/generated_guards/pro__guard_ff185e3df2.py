def guard(features: dict, prediction: str) -> str:
    # Filter trades with low volume but high volatility (potential false breakout)
    if features['volume_ratio'] < 0.6 and features['atr_ratio'] > 1.4:
        return "skip"
    return prediction