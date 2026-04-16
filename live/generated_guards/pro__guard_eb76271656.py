def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation and momentum score strongly disagree."""
    vwap = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Below VWAP but bullish momentum, or above VWAP but bearish momentum
    if (vwap < -0.005 and momentum > 0.15) or (vwap > 0.005 and momentum < -0.15):
        return "skip"
    
    return prediction