def guard(features: dict, prediction: str) -> str:
    """Guard filtering by momentum alignment and candle quality."""
    # Reject trades with momentum contradicting the direction
    momentum = features.get("momentum_score", 0)
    if prediction == "long" and momentum < -0.15:
        return "skip"
    if prediction == "short" and momentum > 0.15:
        return "skip"
    # Reject in low volatility chop
    if features.get("volatility_regime", 1) < 0.35:
        return "skip"
    # Reject candles with excessive wicks (uncertainty)
    total_wick = features.get("upper_wick_ratio", 0) + features.get("lower_wick_ratio", 0)
    if total_wick > 0.65:
        return "skip"
    return prediction