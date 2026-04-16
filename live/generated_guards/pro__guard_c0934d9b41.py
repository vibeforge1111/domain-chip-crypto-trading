def guard(features: dict, prediction: str) -> str:
    """Filter signals where VWAP and momentum disagree."""
    vwap = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == "long":
        # Skip if price below VWAP and negative momentum
        if vwap < -0.001 and momentum < -0.1:
            return "skip"
        # Skip if overbought conditions
        if stoch_k > 80 and stoch_d > 80:
            return "skip"
    elif prediction == "short":
        # Skip if price above VWAP and positive momentum
        if vwap > 0.001 and momentum > 0.1:
            return "skip"
        # Skip if oversold conditions
        if stoch_k < 20 and stoch_d < 20:
            return "skip"
    
    return prediction