def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum decelerates against the signal direction."""
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    
    # Momentum deceleration: long signal but MACD weakening
    if prediction == "long" and (macd < -0.0001 or stoch > 80):
        return "skip"
    # Momentum deceleration: short signal but MACD strengthening  
    if prediction == "short" and (macd > 0.0001 or stoch < 20):
        return "skip"
    return prediction