def guard(features: dict, prediction: str) -> str:
    """Filter trades with extreme wick imbalance or RSI-conflict."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    rsi = features.get('rsi_14', 50)
    
    # Skip long if dominant upper wick (reversal signal)
    if prediction == 'long' and upper_wick > 0.5:
        return "skip"
    
    # Skip short if dominant lower wick (reversal signal)
    if prediction == 'short' and lower_wick > 0.5:
        return "skip"
    
    # Skip if RSI contradicts direction
    if prediction == 'long' and rsi < 30:
        return "skip"
    if prediction == 'short' and rsi > 70:
        return "skip"
    
    return prediction