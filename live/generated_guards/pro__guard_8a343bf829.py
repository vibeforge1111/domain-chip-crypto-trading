def guard(features: dict, prediction: str) -> str:
    """Reject candles dominated by wicks (uncertain price action)."""
    # High wick dominance with small range suggests failed moves
    total_wick = features['upper_wick_ratio'] + features['lower_wick_ratio']
    if total_wick > 0.7 and features['range_pct'] < 0.5:
        return "skip"
    return prediction