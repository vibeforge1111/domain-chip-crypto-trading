def guard(features: dict, prediction: str) -> str:
    """Filter for true compression setups using ATR, BB width, and momentum confirmation."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: elevated ATR with tight BB (impending breakout)
    true_compression = atr_ratio > 1.1 and bb_width < 0.25
    # Momentum confirmation: stochastics aligned
    momentum_ready = (stoch_k > stoch_d and stoch_k < 80) or (stoch_k < stoch_d and stoch_k > 20)
    # VWAP proximity: near key level
    near_vwap = abs(vwap_deviation) < 0.008
    
    if true_compression and momentum_ready and near_vwap:
        return prediction
    
    return "skip"