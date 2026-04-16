def guard(features: dict, prediction: str) -> str:
    """Guard against extreme BB position + RSI conditions indicating potential reversals."""
    bb_pos = features.get("bb_position", 0.5)
    rsi = features.get("rsi_14", 50)
    bb_width = features.get("bb_width", 0)
    
    # Skip if price at extreme BB position AND overbought/oversold
    if (bb_pos > 0.92 and rsi > 70) or (bb_pos < 0.08 and rsi < 30):
        return "skip"
    
    # Also skip if BB is extremely compressed (low bb_width) with extreme position
    if bb_width < 0.5 and (bb_pos > 0.95 or bb_pos < 0.05):
        return "skip"
    
    return prediction