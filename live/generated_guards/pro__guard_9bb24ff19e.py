def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum contradicts entry direction."""
    macd = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect momentum-direction mismatch: entering long without upward momentum
    if prediction == 'long' and macd < 0 and rsi_2h < 70:
        return "skip"
    
    # Entering short without downward momentum
    if prediction == 'short' and macd > 0 and rsi_2h > 30:
        return "skip"
    
    return prediction