def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions as entry zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Extreme BB position: oversold or overbought
    is_extreme_bb = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    # Stochastic confirmation (oversold for longs, overbought for shorts)
    stoch_confirm = (prediction == "long" and stoch_k < 20) or (prediction == "short" and stoch_k > 80)
    
    # Wider RSI context confirms momentum shift
    rsi_confirm = (prediction == "long" and rsi_2h < 40) or (prediction == "short" and rsi_2h > 60)
    
    # Accept trades only at BB extremes with confirmation
    if is_extreme_bb and stoch_confirm and rsi_confirm:
        return prediction
    
    return "skip"