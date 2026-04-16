def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long trades: require positive momentum and not deeply below VWAP
    if prediction == "long":
        if momentum < -0.25 and vwap_dev < -0.01:
            return "skip"
        if rsi_2h > 70:
            return "skip"
    
    # Short trades: require negative momentum and not deeply above VWAP
    if prediction == "short":
        if momentum > 0.25 and vwap_dev > 0.01:
            return "skip"
        if rsi_2h < 30:
            return "skip"
    
    return prediction