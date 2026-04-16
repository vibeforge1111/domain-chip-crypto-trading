def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    # False compression: tight BBs but expanding ATR signals potential fakeout
    if features['bb_width'] < 0.15 and features['atr_ratio'] > 1.25:
        return "skip"
    # Reject extreme stoch readings (reversal zones)
    if features['stoch_k'] > 82 or features['stoch_k'] < 18:
        return "skip"
    # Reject if too far from VWAP
    if abs(features['vwap_deviation']) > 0.012:
        return "skip"
    return prediction