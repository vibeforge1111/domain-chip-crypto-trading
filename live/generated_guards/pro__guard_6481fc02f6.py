def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # High-confidence entry zones: bb_pct_b at extremes
    bb_extreme = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    # Stochastic confirmation for entries
    stoch_confirm = stoch_k < 20 or stoch_k > 80
    
    # Only allow trades when both conditions align
    if not (bb_extreme and stoch_confirm):
        return "skip"
    
    return prediction