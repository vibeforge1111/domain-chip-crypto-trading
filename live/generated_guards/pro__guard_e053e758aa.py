def guard(features: dict, prediction: str) -> str:
    """Guard using BB extremes for high-confidence entries with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long: near lower BB with oversold confirmation
    if bb_pct_b < 0.05 and prediction == "long" and stoch_k < 25 and rsi_2h < 45:
        return prediction
    
    # Short: near upper BB with overbought confirmation
    if bb_pct_b > 0.95 and prediction == "short" and stoch_k > 75 and rsi_2h > 55:
        return prediction
    
    return "skip"