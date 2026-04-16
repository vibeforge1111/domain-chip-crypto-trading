def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Overbought: both Bollinger Band position and Stochastic at extreme highs
    if bb_pct > 0.9 and stoch > 80 and prediction == "long":
        return "skip"
    
    # Oversold: both Bollinger Band position and Stochastic at extreme lows
    if bb_pct < 0.1 and stoch < 20 and prediction == "short":
        return "skip"
    
    return prediction