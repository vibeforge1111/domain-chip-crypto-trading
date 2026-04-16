def guard(features: dict, prediction: str) -> str:
    # Filter trades when momentum is weak AND volatility is elevated
    if features['momentum_score'] < 0.2 and features['atr_ratio'] > 1.3:
        return "skip"
    return prediction