def guard(features: dict, prediction: str) -> str:
    """Custom guard function for BB extreme zone filtering."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # Only trade in extreme BB positions with confirming signals
    if bb_pct_b < 0.05:
        # Lower band - potential long with oversold confirmation
        if rsi_14 < 40 or stoch_k < 30:
            return prediction
    elif bb_pct_b > 0.95:
        # Upper band - potential short with overbought confirmation
        if rsi_14 > 60 or stoch_k > 70:
            return prediction
    
    return "skip"