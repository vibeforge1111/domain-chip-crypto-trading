def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak momentum confirmation at band extremes."""
    momentum = features.get('momentum_score', 0)
    bb_pos = features.get('bb_position', 0.5)
    volume = features.get('volume_ratio', 1)
    rsi = features.get('rsi_14', 50)
    
    # Skip if momentum weak AND at Bollinger Band extremes (potential reversal, not continuation)
    if momentum < 0.3 and (bb_pos < 0.15 or bb_pos > 0.85):
        return "skip"
    
    # Skip if extreme RSI without volume confirmation
    if (rsi > 72 or rsi < 28) and volume < 0.8:
        return "skip"
    
    return prediction