def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration via macd_histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip on bearish momentum (negative histogram suggests deceleration weakening longs)
    if macd_histogram < -0.0002:
        return "skip"
    
    # Skip at stochastic extremes (overbought >80 or oversold <20)
    if stoch_k > 80 or stoch_k < 20:
        return "skip"
    
    return prediction