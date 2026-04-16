def guard(features: dict, prediction: str) -> str:
    """Reject signals with momentum-volume divergence or wick imbalance."""
    momentum = features.get('momentum_score', 0)
    volume = features.get('volume_ratio', 1)
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    
    # Reject: strong momentum but weak volume confirmation
    if abs(momentum) > 0.6 and volume < 0.8:
        return "skip"
    
    # Reject: extreme RSI but price mid-range in bands (weak signal)
    if (rsi > 75 or rsi < 25) and 0.3 < bb_pos < 0.7:
        return "skip"
    
    # Reject long: dominant upper wick suggesting selling pressure
    if prediction == "long" and upper_wick > 0.4:
        return "skip"
    
    # Reject short: dominant lower wick suggesting buying pressure
    if prediction == "short" and lower_wick > 0.4:
        return "skip"
    
    return prediction