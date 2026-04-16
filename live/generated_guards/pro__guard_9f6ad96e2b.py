def guard(features: dict, prediction: str) -> str:
    """Filter trades based on candle quality and momentum alignment."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 0)
    rsi = features.get("rsi_14", 50)
    bb_position = features.get("bb_position", 0.5)
    
    # Reject if candle is primarily wick (doji-like) - unreliable signal
    total_wick = upper_wick + lower_wick
    if total_wick > 0.7 and body_ratio < 0.2:
        return "skip"
    
    # Reject if RSI extreme AND price at Bollinger Band edge (overextended)
    if (rsi > 75 or rsi < 25) and (bb_position < 0.1 or bb_position > 0.9):
        return "skip"
    
    return prediction