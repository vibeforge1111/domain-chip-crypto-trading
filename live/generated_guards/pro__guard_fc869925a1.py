def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree with prediction."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == "long":
        # Reject if price well below VWAP, bearish momentum, and stoch not oversold
        if vwap_dev < -0.015 and momentum < 0 and stoch_k > 30:
            return "skip"
    
    if prediction == "short":
        # Reject if price well above VWAP, bullish momentum, and stoch not overbought
        if vwap_dev > 0.015 and momentum > 0 and stoch_k < 70:
            return "skip"
    
    return prediction