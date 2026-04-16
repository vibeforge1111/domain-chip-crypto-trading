def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch = features.get("stoch_k", 50)
    
    # Long should align: positive momentum + above VWAP (or one offsetting)
    if prediction == "long":
        if momentum < -0.15 and vwap < -0.004:
            return "skip"
        if stoch > 85:
            return "skip"
    # Short should align: negative momentum + below VWAP (or one offsetting)
    elif prediction == "short":
        if momentum > 0.15 and vwap > 0.004:
            return "skip"
        if stoch < 15:
            return "skip"
    
    return prediction