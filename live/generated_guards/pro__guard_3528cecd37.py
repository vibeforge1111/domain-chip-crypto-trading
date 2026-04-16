def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Reject long when price below VWAP with weak momentum and overbought 2h RSI
    if prediction == "long" and vwap_dev < -0.015 and momentum < 0 and rsi_2h > 65:
        return "skip"
    
    # Reject short when price above VWAP with strong momentum and oversold 2h RSI
    if prediction == "short" and vwap_dev > 0.015 and momentum > 0 and rsi_2h < 35:
        return "skip"
    
    return prediction