def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct = features.get('bb_pct_b', 0.5)
    
    vwap_signal = 1 if vwap_dev > 0.002 else -1 if vwap_dev < -0.002 else 0
    momentum_signal = 1 if momentum > 0.05 else -1 if momentum < -0.05 else 0
    
    if vwap_signal != 0 and momentum_signal != 0 and vwap_signal != momentum_signal:
        stoch_conflict = abs(stoch_k - stoch_d) > 15
        bb_extreme = bb_pct < 0.15 or bb_pct > 0.85
        if stoch_conflict or bb_extreme:
            return "skip"
    
    return prediction