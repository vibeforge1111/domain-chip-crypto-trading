def guard(features: dict, prediction: str) -> str:
    """Filter trades based on vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long if price above VWAP but momentum negative (disagreement)
    if prediction == "long" and vwap_dev > 0.004 and momentum < -0.2:
        return "skip"
    
    # Skip short if price below VWAP but momentum positive (disagreement)
    if prediction == "short" and vwap_dev < -0.004 and momentum > 0.2:
        return "skip"
    
    # Filter longs if 2h RSI already overbought (no room to run)
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    
    # Filter shorts if 2h RSI already oversold (no room to fall)
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction