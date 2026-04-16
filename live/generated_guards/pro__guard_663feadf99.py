def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme BB position with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Only filter if bb_pct_b is at extreme zone
    if bb_pct_b < 0.05:
        # Lower band - confirm longs with stoch not oversold and above VWAP
        if prediction == "long" and (stoch_k < 20 or vwap_dev < -0.005):
            return "skip"
    elif bb_pct_b > 0.95:
        # Upper band - confirm shorts with stoch not overbought and below VWAP
        if prediction == "short" and (stoch_k > 80 or vwap_dev > 0.005):
            return "skip"
    
    return prediction