def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to fair value without momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct = features.get('bb_pct_b', 0.5)
    
    # Too close to fair value with weak momentum
    if abs(vwap_dev) < 0.002:
        # Long needs oversold or lower band proximity
        if prediction == "long" and stoch_k > 35 and bb_pct > 0.3:
            return "skip"
        # Short needs overbought or upper band proximity
        if prediction == "short" and stoch_k < 65 and bb_pct < 0.7:
            return "skip"
    
    return prediction