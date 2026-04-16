def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using BB width, ATR ratio, and band position."""
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    vwap_deviation = features.get('vwap_deviation', 0.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Compression detected: BB width below threshold
    compression = bb_width < 0.6
    
    # False compression: tight bands but price at extreme band position
    false_compression = compression and (bb_pct_b < 0.15 or bb_pct_b > 0.85)
    
    # True compression: tight bands with price near middle and low ATR (imminent expansion)
    true_compression = compression and 0.3 <= bb_pct_b <= 0.7 and atr_ratio < 0.85
    
    # Skip if false compression (extreme position + tight bands = trap)
    if false_compression:
        return "skip"
    
    # Skip if compression with stoch divergence (potential reversal)
    if compression and abs(stoch_k - stoch_d) > 20:
        return "skip"
    
    # Skip if compressed but far from VWAP (weak conviction)
    if compression and abs(vwap_deviation) > 0.015:
        return "skip"
    
    return prediction