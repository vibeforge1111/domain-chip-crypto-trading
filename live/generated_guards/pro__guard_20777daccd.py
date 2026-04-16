def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using bb_width, atr_ratio, and new features."""
    bb_width = features.get('bb_width', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: both indicators show low volatility
    is_compressed = bb_width < 0.12 and atr_ratio < 0.75
    
    if is_compressed and prediction != 'skip':
        # False compression signals: near band extremes with weak momentum
        near_extreme = bb_pct_b < 0.1 or bb_pct_b > 0.9
        weak_momentum = stoch_k < 30 or stoch_k > 70
        off_vwap = abs(vwap_dev) > 0.006
        rsi_extreme = rsi_2h < 35 or rsi_2h > 65
        
        # Reject if 3+ false compression signals present
        false_signals = sum([near_extreme, weak_momentum, off_vwap, rsi_extreme])
        if false_signals >= 3:
            return 'skip'
    
    return prediction