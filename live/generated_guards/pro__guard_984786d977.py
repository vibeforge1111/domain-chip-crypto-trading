def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_position = features.get("bb_position", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    body_ratio = features.get("body_ratio", 0.5)
    
    # Skip if candle is a doji (small body) - unreliable signal
    if body_ratio < 0.15:
        return "skip"
    
    # Skip if RSI at extreme and BB at extreme same direction
    if rsi_14 > 70 and bb_position > 0.9:
        return "skip"
    if rsi_14 < 30 and bb_position < 0.1:
        return "skip"
    
    return prediction