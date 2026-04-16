def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Skip long when overbought (BB upper + stochastic overbought)
    if prediction == "long" and bb_pct > 0.9 and stoch > 80:
        return "skip"
    
    # Skip short when oversold (BB lower + stochastic oversold)
    if prediction == "short" and bb_pct < 0.1 and stoch < 20:
        return "skip"
    
    return prediction