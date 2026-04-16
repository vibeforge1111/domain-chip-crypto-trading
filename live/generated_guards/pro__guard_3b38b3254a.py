def guard(features: dict, prediction: str) -> str:
    # Skip if ATR is too compressed (low volatility regime)
    if features.get('atr_ratio', 1) < 0.7:
        return "skip"
    
    # Require volume confirmation for the trade
    if features.get('volume_ratio', 1) < 0.9:
        return "skip"
    
    return prediction