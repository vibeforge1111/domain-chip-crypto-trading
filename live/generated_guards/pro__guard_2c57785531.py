def guard(features: dict, prediction: str) -> str:
    """Filter signals where price is at extreme BB position with overbought/oversold RSI."""
    bb_pos = features.get('bb_position', 0.5)
    rsi = features.get('rsi_14', 50)
    if bb_pos > 0.92 and rsi > 75:
        return "skip"
    if bb_pos < 0.08 and rsi < 25:
        return "skip"
    return prediction