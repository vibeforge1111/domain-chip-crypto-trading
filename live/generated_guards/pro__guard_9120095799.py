def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic extremes."""
    bb = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Reject long signals when both overbought (bb > 0.9 AND stoch > 80)
        if bb > 0.9 and stoch > 80:
            return "skip"
    elif prediction == "short":
        # Reject short signals when both oversold (bb < 0.1 AND stoch < 20)
        if bb < 0.1 and stoch < 20:
            return "skip"
    
    return prediction