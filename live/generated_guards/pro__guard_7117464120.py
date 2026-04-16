def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes and confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    vwap = features.get('vwap_deviation', 0)
    
    # For longs: require lower band extreme AND oversold confirmation
    if prediction == "long" and (bb > 0.20 or stoch > 35):
        return "skip"
    
    # For shorts: require upper band extreme AND overbought confirmation
    if prediction == "short" and (bb < 0.80 or stoch < 65):
        return "skip"
    
    return prediction