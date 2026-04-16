def guard(features: dict, prediction: str) -> str:
    """Filter signals during false compression vs true consolidation."""
    # True compression: BB narrow + price near middle + moderate ATR
    true_compression = features['bb_pct_b'] > 0.25 and features['bb_pct_b'] < 0.75
    
    # False compression signals: stochastic extremes, far from VWAP, momentum divergence
    if true_compression:
        if features['stoch_k'] > 85 or features['stoch_k'] < 15:
            return "skip"
        if abs(features['vwap_deviation']) > 0.015:
            return "skip"
        if features['rsi_2h'] > 70 or features['rsi_2h'] < 30:
            return "skip"
        if features['macd_histogram'] * features['obv_slope'] < 0:
            return "skip"
    return prediction