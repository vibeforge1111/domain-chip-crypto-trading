def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with Stochastic confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long only when price near lower band (bb_pct_b < 0.05) AND oversold (stoch_k < 20)
    if prediction == "long" and bb_pct_b < 0.05 and stoch_k < 20:
        return prediction
    
    # Short only when price near upper band (bb_pct_b > 0.95) AND overbought (stoch_k > 80)
    if prediction == "short" and bb_pct_b > 0.95 and stoch_k > 80:
        return prediction
    
    return "skip"