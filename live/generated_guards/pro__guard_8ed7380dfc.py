def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Long: skip if price extended above VWAP with bearish momentum, or overbought stoch
    if prediction == "long":
        if vwap_dev > 0.005 and momentum < 0:
            return "skip"
        if stoch_k > 80:
            return "skip"
    
    # Short: skip if price extended below VWAP with bullish momentum, or oversold stoch
    if prediction == "short":
        if vwap_dev < -0.005 and momentum > 0:
            return "skip"
        if stoch_k < 20:
            return "skip"
    
    return prediction