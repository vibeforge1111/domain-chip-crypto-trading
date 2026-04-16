def guard(features: dict, prediction: str) -> str:
    """Reject entries when MACD histogram shows momentum deceleration against direction."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Momentum decelerating against the predicted direction
    if prediction == "long" and macd < -0.0002:
        return "skip"
    if prediction == "short" and macd > 0.0002:
        return "skip"
    
    # Additional filter: rejection when overbought/oversold contradicts direction
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction