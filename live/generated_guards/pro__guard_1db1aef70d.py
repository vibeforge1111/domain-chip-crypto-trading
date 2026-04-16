def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes and momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    momentum_score = features.get('momentum_score', 0)
    
    # Extreme lower band - potential long setup
    is_lower_extreme = bb_pct_b < 0.05
    # Extreme upper band - potential short setup
    is_upper_extreme = bb_pct_b > 0.95
    
    # Skip if not at an extreme
    if not is_lower_extreme and not is_upper_extreme:
        return "skip"
    
    # For lower extreme, confirm RSI not oversold too long and momentum not deeply negative
    if is_lower_extreme:
        if rsi_14 < 20 or momentum_score < -0.3:
            return "skip"
        # Accept long signals at lower band with decent RSI
        if prediction == "long":
            return prediction
        return "skip"
    
    # For upper extreme, confirm not overbought and momentum not too positive
    if is_upper_extreme:
        if rsi_14 > 80 or momentum_score > 0.3:
            return "skip"
        # Accept short signals at upper band with decent RSI
        if prediction == "short":
            return prediction
        return "skip"
    
    return "skip"