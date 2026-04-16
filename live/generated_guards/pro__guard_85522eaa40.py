def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using BB extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    volume_ratio = features.get("volume_ratio", 1.0)
    stoch_k = features.get("stoch_k", 50)
    
    # Only allow trades at extreme BB positions (<5th or >95th percentile)
    bb_extreme = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    # Confirm with volume spike (>1.2x average) and extreme stochastic
    volume_confirm = volume_ratio > 1.2
    stoch_extreme = stoch_k < 20 or stoch_k > 80
    
    if bb_extreme and volume_confirm and stoch_extreme:
        return prediction
    
    return "skip"