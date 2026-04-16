def guard(features: dict, prediction: str) -> str:
    """Reject trades too close to VWAP with weak momentum."""
    vwap_dev = abs(features['vwap_deviation'])
    if vwap_dev < 0.005 and features['momentum_score'] < 0:
        return "skip"
    return prediction