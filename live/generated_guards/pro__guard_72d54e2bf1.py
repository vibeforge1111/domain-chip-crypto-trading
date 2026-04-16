def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    Detects true vs false compression using ATR ratio and BB width.
    """
    bb_width = features.get("bb_width", 0.02)
    atr_ratio = features.get("atr_ratio", 1.0)
    vwap_dev = features.get("vwap_deviation", 0.0)
    stoch_k = features.get("stoch_k", 50.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # True compression: low BB width + high ATR ratio (squeeze-breakout)
    # False compression: low BB width + low ATR ratio (dead quiet)
    is_compression = bb_width < 0.03
    is_true_compression = is_compression and atr_ratio > 1.1
    
    # Valid breakout context: near VWAP or reasonable BB position
    vwap_valid = abs(vwap_dev) < 0.005
    
    # Stochastic not in extreme zone (avoids reversal traps)
    stoch_valid = 20 < stoch_k < 80
    
    # BB position not at extreme
    bb_valid = 0.15 < bb_pct_b < 0.85
    
    # Skip if false compression detected (quiet market likely to stay quiet)
    if is_compression and not is_true_compression:
        return "skip"
    
    # Skip if compression without confirmation signals
    if is_compression and (not vwap_valid or not stoch_valid):
        return "skip"
    
    return prediction