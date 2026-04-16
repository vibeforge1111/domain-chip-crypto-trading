def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using BB extremes."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # High-confidence entry zones: BB extreme + overbought/oversold confirmation
    if prediction == "long":
        # Require BB near lower band + stochastic oversold
        if not (bb_pct_b < 0.10 and stoch_k < 30):
            return "skip"
        # Confirm not counter-trend (2h RSI not deeply oversold in downtrend)
        if rsi_2h < 25:
            return "skip"
    
    elif prediction == "short":
        # Require BB near upper band + stochastic overbought
        if not (bb_pct_b > 0.90 and stoch_k > 70):
            return "skip"
        # Confirm not counter-trend (2h RSI not deeply overbought in uptrend)
        if rsi_2h > 75:
            return "skip"
    
    return prediction