def guard(features: dict, prediction: str) -> str:
    """Reject trades where momentum disagrees with candle structure."""
    momentum = features.get('momentum_score', 0)
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 0)
    bb_width = features.get('bb_width', 0)
    
    # Strong momentum but suspicious candle structure = potential rejection
    strong_momentum = abs(momentum) > 0.6
    suspicious_candle = (upper_wick > 0.35 or lower_wick > 0.35) and body_ratio < 0.4
    
    if strong_momentum and suspicious_candle and prediction != "skip":
        # Check if wick contradicts momentum direction
        if momentum > 0 and upper_wick > 0.35:
            return "skip"
        if momentum < 0 and lower_wick > 0.35:
            return "skip"
    
    return prediction