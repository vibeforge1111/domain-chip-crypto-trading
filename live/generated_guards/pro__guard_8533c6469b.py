def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration via MACD histogram with confirmation."""
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    obv = features.get('obv_slope', 0)
    
    # Skip if MACD histogram near zero at stochastic extreme (momentum stalling)
    if abs(macd) < 0.00015 and (stoch > 78 or stoch < 22):
        return "skip"
    # Skip if MACD fading against trade direction with OBV divergence
    if macd < 0 and obv < 0 and prediction == "long":
        return "skip"
    if macd > 0 and obv > 0 and prediction == "short":
        return "skip"
    return prediction