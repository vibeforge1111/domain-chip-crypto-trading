def guard(features: dict, prediction: str) -> str:
    """Detect false compression: tight bands but no directional momentum."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    macd_hist = features.get('macd_histogram', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # True compression present
    compressed = bb_width < 0.15 and atr_ratio < 0.7
    
    # Weak directional signal despite compression
    stoch_neutral = 35 < stoch_k < 65
    rsi_2h_neutral = 40 < rsi_2h < 60
    macd_weak = abs(macd_hist) < 0.0002
    vwap_centered = abs(vwap_dev) < 0.002
    
    if compressed and stoch_neutral and rsi_2h_neutral and macd_weak and vwap_centered:
        return "skip"
    
    return prediction