def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    bb_pos = features.get('bb_pct_b', 0.5)
    
    # Skip trades too close to fair value (low vwap_deviation) with neutral BB position
    if abs(vwap_dev) < 0.003 and 0.35 < bb_pos < 0.65:
        return "skip"
    return prediction