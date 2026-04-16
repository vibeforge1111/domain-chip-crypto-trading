def guard(features: dict, prediction: str) -> str:
    """Guard using bb_pct_b extremes with momentum confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Only trade at extreme bb_pct_b zones
    if bb_pct_b < 0.05:
        # Lower band: long only if stoch confirms oversold and price below VWAP
        if stoch_k > 30 or vwap_deviation > -0.005:
            return "skip"
    elif bb_pct_b > 0.95:
        # Upper band: short only if stoch confirms overbought and price above VWAP
        if stoch_k < 70 or vwap_deviation < 0.005:
            return "skip"
    else:
        return "skip"
    
    return prediction