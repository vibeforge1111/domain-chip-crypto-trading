def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP (fair value) with weak momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Price too close to VWAP with no strong momentum confirmation
    if abs(vwap_dev) < 0.002:
        if prediction == "long" and stoch_k < 40 and bb_pct_b < 0.35:
            return "skip"
        if prediction == "short" and stoch_k > 60 and bb_pct_b > 0.65:
            return "skip"
    
    return prediction