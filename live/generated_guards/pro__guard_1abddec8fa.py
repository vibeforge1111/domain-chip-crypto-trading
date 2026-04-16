def guard(features: dict, prediction: str) -> str:
    """Filters trades where momentum lacks volume confirmation or volatility is unstable."""
    # Skip if high range but low volume (weak conviction move)
    if features['range_pct'] > 0.015 and features['volume_ratio'] < 0.7:
        return "skip"
    # Skip if volatility spike (ATR up) but range stays compressed (unstable)
    if features['atr_ratio'] > 1.4 and features['bb_width'] < 0.8:
        return "skip"
    return prediction