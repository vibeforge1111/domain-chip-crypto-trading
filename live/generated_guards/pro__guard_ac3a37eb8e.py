def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, BB width, and new features."""
    # True compression: low bb_width AND low atr_ratio
    is_compressed = features['bb_width'] < 0.12 and features['atr_ratio'] < 0.6
    
    if is_compressed:
        # False compression at stochastic extremes
        if features['stoch_k'] > 85 or features['stoch_k'] < 15:
            return "skip"
        # False compression far from fair value
        if abs(features['vwap_deviation']) > 0.02:
            return "skip"
        # False compression at Bollinger Band extremes
        if features['bb_pct_b'] > 0.95 or features['bb_pct_b'] < 0.05:
            return "skip"
    return prediction