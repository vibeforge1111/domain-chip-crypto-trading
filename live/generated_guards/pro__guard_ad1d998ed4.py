def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using ATR, BB width, and momentum confirmation."""
    # False compression: BB tight but ATR elevated (volatile breakout coming)
    if features['bb_width'] < 0.15 and features['atr_ratio'] > 1.25:
        return "skip"
    
    # Avoid ranging conditions - require momentum alignment
    if features['stoch_k'] > 30 and features['stoch_k'] < 70:
        return "skip"
    
    # Reject if price too far from VWAP (mean reversion risk)
    if abs(features['vwap_deviation']) > 0.02:
        return "skip"
    
    return prediction