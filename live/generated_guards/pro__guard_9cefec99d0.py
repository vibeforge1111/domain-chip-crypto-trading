def guard(features: dict, prediction: str) -> str:
    """Reject trades when RSI and momentum disagree at BB extremes."""
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0.5)
    bb_pos = features.get('bb_position', 0.5)
    
    # Overbought divergence
    if rsi > 65 and momentum < 0.4 and bb_pos > 0.85:
        return "skip"
    # Oversold divergence
    if rsi < 35 and momentum > 0.6 and bb_pos < 0.15:
        return "skip"
    return prediction