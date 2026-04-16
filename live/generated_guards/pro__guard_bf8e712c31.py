def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum shows deceleration via macd_histogram."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Momentum flattening: macd histogram near zero + stochastic divergence
    if abs(macd) < 0.0002 and stoch_k < stoch_d:
        return "skip"
    
    return prediction