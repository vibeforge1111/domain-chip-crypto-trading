def guard(features: dict, prediction: str) -> str:
    """Reject trades where VWAP and momentum disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip longs if price below VWAP but momentum is bullish (divergence warning)
    if prediction == 'long' and vwap_dev < -0.003 and momentum > 0.1:
        return "skip"
    
    # Skip shorts if price above VWAP but momentum is bearish (divergence warning)
    if prediction == 'short' and vwap_dev > 0.003 and momentum < -0.1:
        return "skip"
    
    return prediction