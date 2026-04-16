def guard(features: dict, prediction: str) -> str:
    """Guard using BB extremes as high-confidence zones with RSI_2H confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Only accept trades in extreme BB zones (<0.1 or >0.9)
    if bb_pct_b < 0.1 or bb_pct_b > 0.9:
        # Confirm with RSI_2H: longs need bullish (rsi_2h > 40), shorts need bearish (rsi_2h < 60)
        if prediction == "long" and rsi_2h <= 40:
            return "skip"
        if prediction == "short" and rsi_2h >= 60:
            return "skip"
        return prediction
    
    return "skip"