def guard(features: dict, prediction: str) -> str:
    """Filter trades using BB extremes with confirmation from stochastic and VWAP."""
    bb = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Long: require BB near lower band AND stochastic oversold
    if prediction == "long":
        if not (bb < 0.10 and stoch_k < 30):
            return "skip"
    
    # Short: require BB near upper band AND stochastic overbought
    if prediction == "short":
        if not (bb > 0.90 and stoch_k > 70):
            return "skip"
    
    return prediction