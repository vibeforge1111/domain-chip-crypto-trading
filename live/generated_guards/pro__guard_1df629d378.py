def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration using macd_histogram with confirmation."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    bb_pos = features.get("bb_pct_b", 0.5)
    
    # Momentum deceleration with stochastic confirmation at band extremes
    if prediction == "long" and macd < -0.0002 and stoch_k < 30 and bb_pos > 0.75:
        return "skip"
    if prediction == "short" and macd > 0.0002 and stoch_k > 70 and bb_pos < 0.25:
        return "skip"
    
    return prediction