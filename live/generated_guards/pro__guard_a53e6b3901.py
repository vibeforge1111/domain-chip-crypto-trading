def guard(features: dict, prediction: str) -> str:
    """Filter trades when volume spikes with tight range and heavy wicks (distribution/accumulation)."""
    if prediction != "skip":
        high_volume = features['volume_ratio'] > 1.5
        tight_range = features['range_pct'] < features.get('atr_ratio', 0.5) * 0.7
        wick_heavy = (features['upper_wick_ratio'] + features['lower_wick_ratio']) > 0.65
        
        if high_volume and tight_range and wick_heavy:
            return "skip"
    return prediction