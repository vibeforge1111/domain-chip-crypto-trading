def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extreme positions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Only allow entries at extreme BB positions
    extreme_bb = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    if not extreme_bb:
        return "skip"
    
    # For long signals at lower band, check oversold stochastic confirmation
    if prediction == "long" and bb_pct_b < 0.05:
        if stoch_k > 20:  # Stochastic already leaving oversold
            return "skip"
    
    # For short signals at upper band, check overbought stochastic confirmation
    if prediction == "short" and bb_pct_b > 0.95:
        if stoch_k < 80:  # Stochastic not yet in overbought
            return "skip"
    
    # Ensure wider RSI context aligns with direction
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction