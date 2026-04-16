def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions as high-confidence zones."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    
    # High-confidence long: bb_pct_b < 0.05 (at lower band) with RSI confirmation
    if prediction == "long" and bb_pct_b < 0.05:
        if rsi_14 > 30:  # Not deeply oversold
            return prediction
    
    # High-confidence short: bb_pct_b > 0.95 (at upper band) with RSI confirmation
    if prediction == "short" and bb_pct_b > 0.95:
        if rsi_14 < 70:  # Not deeply overbought
            return prediction
    
    return "skip"