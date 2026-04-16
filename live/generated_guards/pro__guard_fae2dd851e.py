def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP position and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    if prediction == "long":
        # Long position but price below VWAP AND momentum bearish
        if vwap_dev < -0.005 and momentum < 0:
            return "skip"
    elif prediction == "short":
        # Short position but price above VWAP AND momentum bullish
        if vwap_dev > 0.005 and momentum > 0:
            return "skip"
    
    return prediction