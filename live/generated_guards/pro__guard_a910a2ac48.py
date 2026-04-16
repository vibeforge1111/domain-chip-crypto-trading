def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == "long":
        # Skip if bearish setup: price below VWAP, negative momentum, oversold stoch
        if vwap_dev < -0.003 and momentum < 0 and stoch_k < 30:
            return "skip"
    
    elif prediction == "short":
        # Skip if bullish setup: price above VWAP, positive momentum, overbought stoch
        if vwap_dev > 0.003 and momentum > 0 and stoch_k > 70:
            return "skip"
    
    return prediction