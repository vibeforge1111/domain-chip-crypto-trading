def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Only allow entries at BB extremes (<0.05 oversold, >0.95 overbought)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Longs require oversold extreme + price below VWAP
    if prediction == "long" and not (bb_pct_b < 0.05 and vwap_deviation < 0):
        return "skip"
    
    # Shorts require overbought extreme + price above VWAP
    if prediction == "short" and not (bb_pct_b > 0.95 and vwap_deviation > 0):
        return "skip"
    
    return prediction