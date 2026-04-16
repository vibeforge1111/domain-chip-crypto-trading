def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extremes with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # High-confidence entry zones: BB extremes
    in_lower_extreme = bb_pct_b < 0.05
    in_upper_extreme = bb_pct_b > 0.95
    
    # Only accept trades at BB extremes
    if not (in_lower_extreme or in_upper_extreme):
        return "skip"
    
    # Long entry: lower extreme with oversold confirmation
    if prediction == "long":
        if not in_lower_extreme:
            return "skip"
        if stoch_k > 20 or stoch_d > 25:
            return "skip"
        if rsi_2h > 60:
            return "skip"
    
    # Short entry: upper extreme with overbought confirmation
    if prediction == "short":
        if not in_upper_extreme:
            return "skip"
        if stoch_k < 80 or stoch_d > 85:
            return "skip"
        if rsi_2h < 40:
            return "skip"
    
    return prediction