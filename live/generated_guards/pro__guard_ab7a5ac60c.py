def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Filter longs: need bullish stochastic alignment and favorable wider context
    if prediction == "long":
        # Reject if stochastic showing bearish alignment
        if stoch_k < stoch_d:
            return "skip"
        # Reject if overbought and near upper BB
        if stoch_k > 75 and bb_pct_b > 0.85:
            return "skip"
        # Reject if 2h RSI shows bearish divergence
        if rsi_2h < 40 and stoch_k < 40:
            return "skip"
    
    # Filter shorts: need bearish stochastic alignment
    elif prediction == "short":
        if stoch_k > stoch_d:
            return "skip"
        if stoch_k < 25 and bb_pct_b < 0.15:
            return "skip"
        if rsi_2h > 60 and stoch_k > 60:
            return "skip"
    
    return prediction