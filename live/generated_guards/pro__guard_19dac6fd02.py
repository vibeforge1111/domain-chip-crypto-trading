def guard(features: dict, prediction: str) -> str:
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Detect compression: low ATR and tight BB width
    in_compression = atr_ratio < 0.7 and bb_width < 0.5
    
    if in_compression and prediction != "skip":
        # False compression signals: no clear directional conviction
        # Price stuck in middle of bands
        bb_neutral = 0.35 < bb_pct_b < 0.65
        # Stochastic flat/stochastic not aligned
        stoch_flat = abs(stoch_k - stoch_d) < 5
        # No momentum direction
        macd_weak = abs(macd_histogram) < 0.0001
        # No VWAP conviction
        vwap_neutral = abs(vwap_deviation) < 0.003
        
        # All conditions suggest random breakout likely
        if bb_neutral and stoch_flat and macd_weak and vwap_neutral:
            return "skip"
    
    return prediction