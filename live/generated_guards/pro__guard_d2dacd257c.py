def guard(features: dict, prediction: str) -> str:
    # Reject overextended positions at band extremes with extreme RSI (mean reversion risk)
    bb_pos = features.get('bb_position', 0.5)
    rsi = features.get('rsi_14', 50)
    
    if bb_pos > 0.9 and rsi > 70:
        return "skip"
    if bb_pos < 0.1 and rsi < 30:
        return "skip"
    
    return prediction