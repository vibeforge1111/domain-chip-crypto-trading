def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Long: extreme lower BB + oversold stochastic + below VWAP
    if bb_pct_b < 0.05 and prediction == "long":
        if stoch_k < 30 and vwap_deviation < 0:
            return prediction
    
    # Short: extreme upper BB + overbought stochastic + above VWAP
    if bb_pct_b > 0.95 and prediction == "short":
        if stoch_k > 70 and vwap_deviation > 0:
            return prediction
    
    return "skip"