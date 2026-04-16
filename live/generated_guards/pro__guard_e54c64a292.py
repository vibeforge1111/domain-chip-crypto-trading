def guard(features: dict, prediction: str) -> str:
    """Guard against overbought/oversold extremes using Bollinger Bands and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Skip longs at overbought extremes (both indicators confirm)
    if prediction == "long" and bb_pct > 0.88 and stoch > 80:
        return "skip"
    
    # Skip shorts at oversold extremes (both indicators confirm)
    if prediction == "short" and bb_pct < 0.12 and stoch < 20:
        return "skip"
    
    return prediction