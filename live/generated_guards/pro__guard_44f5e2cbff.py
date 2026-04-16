def guard(features: dict, prediction: str) -> str:
    bb_width = features.get('bb_width', 0.5)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    obv_slope = features.get('obv_slope', 0)
    
    # False compression: tight bands + very low ATR = dead market, skip
    if bb_width < 0.15 and atr_ratio < 0.7:
        return "skip"
    
    # Valid compression needs aligned momentum + VWAP neutrality
    momentum_aligned = abs(stoch_k - stoch_d) < 20
    vwap_central = abs(vwap_deviation) < 0.005
    volume_confirming = obv_slope > 0 if prediction == "long" else obv_slope < 0
    
    # If compression but indicators disagree, likely false breakout
    if bb_width < 0.2 and not (momentum_aligned and vwap_central):
        return "skip"
    
    return prediction