def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum divergence or dangerous volatility spikes."""
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if RSI extreme AND price at BB extremes (potential reversal)
    if (rsi > 70 or rsi < 30) and (bb_pos > 0.9 or bb_pos < 0.1):
        return "skip"
    
    # Skip if volatility spike (dangerous)
    if atr_ratio > 2.0:
        return "skip"
    
    return prediction