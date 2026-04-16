def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions with stochastics."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # At extreme lower band - only accept longs if stoch confirms oversold
    if bb_pct_b < 0.05:
        if stoch_k < 20 and stoch_d < 20:
            return prediction
        return "skip"
    
    # At extreme upper band - only accept shorts if stoch confirms overbought
    if bb_pct_b > 0.95:
        if stoch_k > 80 and stoch_d > 80:
            return prediction
        return "skip"
    
    return prediction