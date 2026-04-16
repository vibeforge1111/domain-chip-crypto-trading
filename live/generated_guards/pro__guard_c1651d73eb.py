def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip long if overbought on both BB and stochastic
    if prediction == "long" and bb_pct > 0.80 and stoch_k > 75:
        return "skip"
    
    # Skip short if oversold on both BB and stochastic
    if prediction == "short" and bb_pct < 0.20 and stoch_k < 25:
        return "skip"
    
    return prediction