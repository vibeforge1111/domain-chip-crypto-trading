def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject longs when deeply oversold (both indicators confirm)
    if prediction == "long" and bb < 0.15 and stoch < 20:
        return "skip"
    
    # Reject shorts when deeply overbought (both indicators confirm)
    if prediction == "short" and bb > 0.85 and stoch > 80:
        return "skip"
    
    return prediction