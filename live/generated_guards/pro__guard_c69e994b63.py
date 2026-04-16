def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # High-confidence zones only: extreme bb_pct_b positions
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    # For longs at lower band, confirm not a falling knife (stoch not deeply oversold)
    if prediction == "long" and stoch_k < 10:
        return "skip"
    
    # For shorts at upper band, confirm not strong momentum (rsi_2h not too bullish)
    if prediction == "short" and rsi_2h > 70:
        return "skip"
    
    return prediction