def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions with momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Only trade at extreme BB positions with confirming momentum
    if bb_pct_b < 0.05 and stoch_k > 20:  # Lower extreme + turning up
        return prediction
    elif bb_pct_b > 0.95 and stoch_k < 80:  # Upper extreme + turning down
        return prediction
    
    return "skip"