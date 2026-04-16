def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression using atr_ratio, bb_width and momentum confirmation."""
    bb_width = features.get("bb_width", 0.02)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # Detect compression: both low volatility and narrow bands
    in_compression = atr_ratio < 0.7 and bb_width < 0.015
    
    if in_compression:
        # Reject if position is at extreme within bands (potential trap)
        if bb_pct_b < 0.1 or bb_pct_b > 0.9:
            return "skip"
        # Reject if stochastic divergent (momentum weakening)
        if abs(stoch_k - stoch_d) > 15:
            return "skip"
        # Reject if wider timeframe RSI extreme (context divergence)
        if rsi_2h < 30 or rsi_2h > 70:
            return "skip"
    
    return prediction