def guard(features: dict, prediction: str) -> str:
    """Filter trades on extreme RSI with concurrent Bollinger Band position extremes."""
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    
    if rsi > 68 and bb_pos > 0.92:
        return "skip"
    if rsi < 32 and bb_pos < 0.08:
        return "skip"
    
    return prediction