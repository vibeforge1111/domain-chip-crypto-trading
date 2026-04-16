def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak candle structure and poor momentum alignment."""
    body_ratio = features.get("body_ratio", 1.0)
    upper_wick_ratio = features.get("upper_wick_ratio", 0.0)
    lower_wick_ratio = features.get("lower_wick_ratio", 0.0)
    bb_position = features.get("bb_position", 0.5)
    momentum_score = features.get("momentum_score", 0.0)
    volume_ratio = features.get("volume_ratio", 1.0)
    rsi_14 = features.get("rsi_14", 50)
    
    # Skip if candle is a doji (tiny body, large wicks) - indecision
    if body_ratio < 0.2 and (upper_wick_ratio + lower_wick_ratio) > 0.6:
        return "skip"
    
    # Skip if deeply overbought/oversold without momentum confirmation
    if bb_position > 0.9 and momentum_score < 0:
        return "skip"
    if bb_position < 0.1 and momentum_score > 0:
        return "skip"
    
    # Skip if low volume with extreme BB position - weak conviction
    if volume_ratio < 0.5 and (bb_position > 0.85 or bb_position < 0.15):
        return "skip"
    
    # Skip if RSI extreme with opposing candle structure
    if rsi_14 > 75 and lower_wick_ratio > upper_wick_ratio * 2:
        return "skip"
    if rsi_14 < 25 and upper_wick_ratio > lower_wick_ratio * 2:
        return "skip"
    
    return prediction