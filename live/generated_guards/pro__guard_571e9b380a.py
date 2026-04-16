def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extremes and mean reversion confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Lower extreme: only accept longs with oversold confirmation
    if bb_pct_b < 0.05:
        if prediction == "long" and (stoch_k < 20 or stoch_d < 20):
            return prediction
        return "skip"
    
    # Upper extreme: only accept shorts with overbought confirmation
    if bb_pct_b > 0.95:
        if prediction == "short" and (stoch_k > 80 or stoch_d > 80):
            return prediction
        return "skip"
    
    # Middle zone: skip non-extreme entries
    return "skip"