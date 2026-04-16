def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using stochastic crossover timing."""
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    obv_slope = features.get("obv_slope", 0)
    
    # Calculate stochastic spread (positive = k above d, bullish)
    stoch_spread = stoch_k - stoch_d
    
    if prediction == "long":
        # Require bullish stochastic alignment (k crossed above d)
        if stoch_spread < 0:
            return "skip"
        # Reject if overbought (stochastic > 80) - reversal risk
        if stoch_k > 80:
            return "skip"
        # Require price above VWAP for long confirmation
        if vwap_dev < 0:
            return "skip"
        # Confirm with wider timeframe RSI not overbought
        if rsi_2h > 70:
            return "skip"
    
    elif prediction == "short":
        # Require bearish stochastic alignment (k crossed below d)
        if stoch_spread > 0:
            return "skip"
        # Reject if oversold (stochastic < 20) - reversal risk
        if stoch_k < 20:
            return "skip"
        # Require price below VWAP for short confirmation
        if vwap_dev > 0:
            return "skip"
        # Confirm with wider timeframe RSI not oversold
        if rsi_2h < 30:
            return "skip"
    
    return prediction