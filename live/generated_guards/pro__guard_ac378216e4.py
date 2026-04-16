def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    
    # Long signals need price above VWAP and positive momentum
    if prediction == "long":
        if vwap_dev < -0.002 and momentum < 0:
            return "skip"
        # Reject longs when stoch is overbought and price far below VWAP
        if stoch_k > 80 and vwap_dev < -0.005:
            return "skip"
    
    # Short signals need price below VWAP and negative momentum
    elif prediction == "short":
        if vwap_dev > 0.002 and momentum > 0:
            return "skip"
        # Reject shorts when stoch is oversold and price far above VWAP
        if stoch_k < 20 and vwap_dev > 0.005:
            return "skip"
    
    return prediction