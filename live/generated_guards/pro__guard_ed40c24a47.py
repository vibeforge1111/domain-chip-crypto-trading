def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject longs when broader 2h trend is overbought (exhausted)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    # Reject shorts when broader 2h trend is oversold (exhausted)  
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction