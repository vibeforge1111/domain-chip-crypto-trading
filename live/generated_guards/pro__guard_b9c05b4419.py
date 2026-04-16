def guard(features: dict, prediction: str) -> str:
    """Filter based on volatility regime context."""
    # Focus on productive volatility regime
    if features['volatility_regime'] != 'event_driven,range':
        return "skip"
    # Skip extreme ATR conditions (compressed or expanded)
    if features['atr_ratio'] < 0.5 or features['atr_ratio'] > 2.0:
        return "skip"
    return prediction