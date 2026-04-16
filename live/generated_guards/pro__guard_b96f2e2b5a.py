def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to filter bad trades."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression: low BB width and low ATR
    is_compressed = bb_width < 0.85 and atr_ratio < 0.85
    
    # False compression indicators
    # Price stuck in middle of bands (no directional bias)
    no_band_position = abs(bb_pct_b - 0.5) < 0.15
    # Stochastic flat without direction
    stoch_flat = abs(stoch_k - stoch_d) < 5 and 30 < stoch_k < 70
    # No momentum building (flat MACD and OBV)
    no_momentum = abs(macd_histogram) < 0.0002 and abs(obv_slope) < 0.01
    
    # Skip false compression setups
    if is_compressed and no_band_position and stoch_flat and no_momentum:
        return "skip"
    
    return prediction