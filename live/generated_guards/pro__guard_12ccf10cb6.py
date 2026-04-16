def guard(features: dict, prediction: str) -> str:
    """Reject signals where VWAP deviation conflicts with momentum score."""
    # Skip if price stretched above VWAP but momentum weak
    if features['vwap_deviation'] > 0.015 and features['momentum_score'] < 40:
        return "skip"
    # Skip if price stretched below VWAP but momentum strong
    if features['vwap_deviation'] < -0.015 and features['momentum_score'] > 60:
        return "skip"
    return prediction