def guard(features: dict, prediction: str) -> str:
    """Filter trades based on MACD momentum alignment and strength."""
    macd = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Momentum must align with prediction direction
    if prediction == "long" and macd < 0:
        return "skip"
    if prediction == "short" and macd > 0:
        return "skip"
    
    # Reject weak momentum signals
    if abs(macd) < 0.0001:
        return "skip"
    
    # Additional filter: avoid entries against 2h trend
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction