def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2-hour trend context."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Longs require some bullishness in broader trend
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    
    # Shorts require some bearishness in broader trend
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction