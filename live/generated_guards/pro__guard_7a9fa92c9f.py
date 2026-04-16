def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Filter longs when overbought: bb upper band + stoch > 80
    if prediction == "long" and bb_pct > 0.88 and stoch > 80:
        return "skip"
    
    # Filter shorts when oversold: bb lower band + stoch < 20
    if prediction == "short" and bb_pct < 0.12 and stoch < 20:
        return "skip"
    
    return prediction