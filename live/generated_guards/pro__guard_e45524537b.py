def guard(features: dict, prediction: str) -> str:
    """Reject trades where VWAP deviation and momentum score disagree."""
    # Price too far above VWAP but momentum fading
    if features['vwap_deviation'] > 0.015 and features['momentum_score'] < -0.1:
        return "skip"
    # Price too far below VWAP but momentum building
    if features['vwap_deviation'] < -0.015 and features['momentum_score'] > 0.1:
        return "skip"
    return prediction