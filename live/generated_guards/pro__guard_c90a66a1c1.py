def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    bullish_signals = sum([
        bb_pct_b < 0.35,  # Near lower BB
        vwap_deviation < -0.005,  # Below VWAP
        stoch_k < 25,  # Stochastic oversold
        obv_slope > 0,  # Volume accumulation
        macd_histogram > 0,  # MACD bullish
        rsi_2h > 45  # 2h context not weak
    ])
    
    bearish_signals = sum([
        bb_pct_b > 0.65,  # Near upper BB
        vwap_deviation > 0.005,  # Above VWAP
        stoch_k > 75,  # Stochastic overbought
        obv_slope < 0,  # Volume distribution
        macd_histogram < 0,  # MACD bearish
        rsi_2h < 55  # 2h context not strong
    ])
    
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction