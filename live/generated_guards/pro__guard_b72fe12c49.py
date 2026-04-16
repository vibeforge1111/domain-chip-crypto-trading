def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum deceleration."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Momentum flattening (histogram near zero) combined with extreme stoch
    if abs(macd) < 0.0001 and (stoch_k > 75 or stoch_k < 25):
        return "skip"
    return prediction