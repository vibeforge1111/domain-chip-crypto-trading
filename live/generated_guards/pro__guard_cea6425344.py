def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes as high-confidence entry zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Only accept trades at BB extremes (<0.05 or >0.95)
    # Confirm with stochastic for additional validation
    at_lower_extreme = bb_pct_b < 0.05 and stoch_k < 20
    at_upper_extreme = bb_pct_b > 0.95 and stoch_k > 80
    
    if at_lower_extreme or at_upper_extreme:
        return prediction
    
    return "skip"