def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using ATR + Bollinger analysis."""
    is_compressed = features.get('atr_ratio', 1) < 0.75 and features.get('bb_width', 1) < 0.35
    
    if is_compressed:
        bb_extreme = features.get('bb_pct_b', 0.5) < 0.12 or features.get('bb_pct_b', 0.5) > 0.88
        weak_momentum = features.get('macd_histogram', 0) < -0.0001 and features.get('rsi_2h', 50) < 40
        stoch_diverge = features.get('stoch_k', 50) - features.get('stoch_d', 50) < -5
        
        if bb_extreme and (weak_momentum or stoch_diverge):
            return "skip"
    
    return prediction