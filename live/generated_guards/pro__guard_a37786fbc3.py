def guard(features: dict, prediction: str) -> str:
    """Custom guard function for filtering false compression breakouts.

    Detects true vs false compression using atr_ratio, bb_width, and new features
    to identify when narrowing bands are likely to produce failed breakouts.
    """
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect compression: both atr_ratio and bb_width are low
    in_compression = atr_ratio < 0.7 and bb_width < 0.15
    
    if in_compression:
        # False compression signals to reject:
        # 1. Price at BB extremes (reversal likely)
        at_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
        # 2. Stochastic divergence during compression
        stoch_diverging = abs(stoch_k - stoch_d) > 20
        # 3. Volume declining during compression
        volume_drying = obv_slope < -0.1
        # 4. RSI in wrong context for prediction direction
        rsi_conflict = (prediction == "long" and rsi_2h < 35) or (prediction == "short" and rsi_2h > 65)
        
        if at_extreme or stoch_diverging or volume_drying or rsi_conflict:
            return "skip"
    
    return prediction