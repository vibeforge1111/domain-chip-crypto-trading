def guard(features: dict, prediction: str) -> str:
    """Detect squeeze compression and skip extreme positions prone to false breakouts."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 0.02)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # True squeeze: low ATR + narrow BB
    squeeze = atr_ratio < 0.8 and bb_width < 0.015
    
    if squeeze:
        # Price at extreme + overbought/oversold = likely false compression
        if (bb_pct_b < 0.15 or bb_pct_b > 0.85) and (stoch_k < 20 or stoch_k > 80):
            return "skip"
    
    return prediction