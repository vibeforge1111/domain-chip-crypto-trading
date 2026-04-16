def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating against the direction."""
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration: long without bullish histogram, or short without bearish
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Overbought/oversold divergence with wider timeframe
    if prediction == "long" and stoch_k > 80 and rsi_2h > 65:
        return "skip"
    if prediction == "short" and stoch_k < 20 and rsi_2h < 35:
        return "skip"
    
    return prediction