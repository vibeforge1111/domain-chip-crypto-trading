def guard(features: dict, prediction: str) -> str:
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Reject long when at upper band extreme AND overbought stochastic
    if prediction == "long" and bb > 0.88 and stoch > 75:
        return "skip"
    
    # Reject short when at lower band extreme AND oversold stochastic
    if prediction == "short" and bb < 0.12 and stoch < 25:
        return "skip"
    
    return prediction