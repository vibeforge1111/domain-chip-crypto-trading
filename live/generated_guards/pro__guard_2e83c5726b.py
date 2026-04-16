def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when overbought: bb at upper band AND stoch extreme
    if prediction == "long" and bb > 0.88 and stoch > 80:
        return "skip"
    
    # Skip shorts when oversold: bb at lower band AND stoch extreme
    if prediction == "short" and bb < 0.12 and stoch < 20:
        return "skip"
    
    # Additional filter: rsi_2h confirmation
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction