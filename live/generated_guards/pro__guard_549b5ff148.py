def guard(features: dict, prediction: str) -> str:
    """Reject trades during Bollinger Band squeeze with extreme position (false breakout risk)."""
    bb_width = features.get("bb_width", 0.5)
    bb_position = features.get("bb_position", 0.5)
    
    # Squeeze conditions: low bandwidth + extreme position = likely false breakout
    squeeze = bb_width < 0.3
    extreme = bb_position > 0.85 or bb_position < 0.15
    
    if squeeze and extreme:
        return "skip"
    
    return prediction