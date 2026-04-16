def guard(features: dict, prediction: str) -> str:
    """Reject trades on low-conviction candles (wick-dominated) with weak momentum."""
    wick_total = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Skip if candle is mostly wicks (uncertainty) AND momentum is weak
    if wick_total > 0.6 and body_ratio < 0.25 and momentum_score < 0.3:
        return "skip"
    return prediction