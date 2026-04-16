def guard(features: dict, prediction: str) -> str:
    """Filter trades using 2h RSI alignment with broader trend and momentum."""
    rsi_2h = features.get("rsi_2h", 50)
    rsi_14 = features.get("rsi_14", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Align long entries with bullish broader trend
    if prediction == "long" and rsi_2h < 42:
        return "skip"
    
    # Align short entries with bearish broader trend
    if prediction == "short" and rsi_2h > 58:
        return "skip"
    
    # Avoid buying at upper Bollinger Band extreme with overbought short-term
    if prediction == "long" and bb_pct_b > 0.88 and stoch_k > 75:
        return "skip"
    
    return prediction