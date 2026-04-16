def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip long if overbought (high BB position + overbought stochastic)
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 75:
        return "skip"
    
    # Skip short if oversold (low BB position + oversold stochastic)
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 25:
        return "skip"
    
    return prediction