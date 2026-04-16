def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # True compression: low volatility + tight bands
    is_compressed = atr_ratio < 0.75 and bb_width < 0.25
    
    # False compression indicators
    extreme_stoch = stoch_k > 85 or stoch_k < 15
    rsi_extreme = rsi_2h > 70 or rsi_2h < 30
    near_band_edge = bb_pct_b > 0.9 or bb_pct_b < 0.1
    
    # Reject if compressed but with conflicting signals (potential false move)
    if is_compressed and (extreme_stoch or rsi_extreme or near_band_edge):
        return "skip"
    
    return prediction