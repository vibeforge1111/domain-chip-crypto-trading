def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_14 = features.get('rsi_14', 50)
    
    # Long at lower band with oversold confirmation
    if bb_pct_b < 0.05 and prediction == "long":
        if stoch_k < 25 or rsi_14 < 35:
            return prediction
        return "skip"
    
    # Short at upper band with overbought confirmation
    if bb_pct_b > 0.95 and prediction == "short":
        if stoch_k > 75 or rsi_14 > 65:
            return prediction
        return "skip"
    
    return "skip"