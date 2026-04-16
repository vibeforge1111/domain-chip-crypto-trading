def guard(features: dict, prediction: str) -> str:
    """Detect false compression: high volatility expansion but bands not actually compressing."""
    # False compression: high atr_ratio but bb_width remains elevated
    if features['atr_ratio'] > 1.4 and features['bb_width'] > 0.6:
        return "skip"
    # Skip extreme stochastic readings
    if features['stoch_k'] > 85 or features['stoch_k'] < 15:
        return "skip"
    # Skip when far from VWAP (mean reversion risk)
    if abs(features['vwap_deviation']) > 0.015:
        return "skip"
    return prediction