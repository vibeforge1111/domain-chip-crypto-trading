def guard(features: dict, prediction: str) -> str:
    """Reject signals misaligned with the 2-hour broader trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject long entries when higher timeframe RSI is overbought
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Reject short entries when higher timeframe RSI is oversold
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction