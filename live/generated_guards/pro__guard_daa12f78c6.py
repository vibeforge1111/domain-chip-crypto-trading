def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score strongly disagree."""
    vwap = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch = features.get('stoch_k', 50)
    
    # Skip when price above VWAP but momentum bearish (confirmed by stoch)
    if vwap > 0.003 and momentum < -0.05 and stoch < 40:
        return "skip"
    # Skip when price below VWAP but momentum bullish (confirmed by stoch)
    if vwap < -0.003 and momentum > 0.05 and stoch > 60:
        return "skip"
    
    return prediction