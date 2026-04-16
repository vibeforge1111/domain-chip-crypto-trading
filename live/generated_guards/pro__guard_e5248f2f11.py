def guard(features: dict, prediction: str) -> str:
    """Custom guard function using rsi_2h to align entries with broader trend."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Reject long signals when broader timeframe is overbought
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    
    # Reject short signals when broader timeframe is oversold
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    # Additional filter: avoid counter-trend longs with extended stochastic
    if prediction == "long" and rsi_2h > 60 and stoch_k > 80 and bb_pct_b > 0.85:
        return "skip"
    
    return prediction