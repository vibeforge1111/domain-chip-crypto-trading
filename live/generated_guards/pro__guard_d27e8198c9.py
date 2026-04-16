def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 0.2)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # False compression: tight bands but volatility rising (fakeout likely)
    if bb_width < 0.15 and atr_ratio > 1.2:
        return "skip"
    
    # Compression without momentum: mid-band squeeze, weak setup
    if bb_width < 0.18 and abs(bb_pct_b - 0.5) < 0.15 and stoch_k < 35 and rsi_2h < 45:
        return "skip"
    
    return prediction