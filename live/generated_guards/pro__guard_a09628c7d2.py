def guard(features: dict, prediction: str) -> str:
    """Use 2-hour RSI to align entries with broader trend context."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject longs when broader trend is weak (oversold)
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    # Reject shorts when broader trend is strong (overbought continuation risk)
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    return prediction