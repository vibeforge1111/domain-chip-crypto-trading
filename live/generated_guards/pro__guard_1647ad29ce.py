def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI-BB divergence and wick rejection patterns."""
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    
    # Reject when RSI extreme AND price at opposite band edge (reversal risk)
    if rsi > 75 and bb_pos > 0.88:
        return "skip"
    if rsi < 25 and bb_pos < 0.12:
        return "skip"
    
    # Reject wick rejections against predicted direction
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    
    if prediction == "long" and upper_wick > 0.4 and upper_wick > lower_wick * 1.5:
        return "skip"
    if prediction == "short" and lower_wick > 0.4 and lower_wick > upper_wick * 1.5:
        return "skip"
    
    return prediction