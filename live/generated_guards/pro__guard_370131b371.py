def guard(features: dict, prediction: str) -> str:
    """Filter trades using RSI-momentum divergence and BB-range interaction."""
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    bb_pos = features.get('bb_position', 0.5)
    range_pct = features.get('range_pct', 0)
    
    # Reject long when RSI extremely overbought AND momentum contradicts
    if prediction == 'long' and rsi > 75 and momentum < -0.2:
        return 'skip'
    # Reject short when RSI extremely oversold AND momentum contradicts
    if prediction == 'short' and rsi < 25 and momentum > 0.2:
        return 'skip'
    
    # Reject when price at BB extreme but range is small (choppy squeeze)
    if (bb_pos > 0.95 or bb_pos < 0.05) and range_pct < 0.35:
        return 'skip'
    
    return prediction