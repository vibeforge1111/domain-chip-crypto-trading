def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme BB zones with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Must be in extreme BB zone (<0.05 or >0.95) for valid entry
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # At lower band: only allow longs, require oversold confirmation
    if bb_pct_b < 0.05:
        if prediction == "short":
            return "skip"
        if stoch_k >= 20:
            return "skip"
    
    # At upper band: only allow shorts, require overbought confirmation
    if bb_pct_b > 0.95:
        if prediction == "long":
            return "skip"
        if stoch_k <= 80:
            return "skip"
    
    return prediction