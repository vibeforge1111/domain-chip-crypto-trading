def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak candle structure or momentum-trend divergence."""
    # Reject if candle has poor structure (small body, large wicks = weak signal)
    candle_strength = features.get('body_ratio', 0) - (features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0))
    if candle_strength < 0.1:
        return "skip"
    # Reject if momentum contradicts trend direction
    momentum_trend_product = features.get('momentum_score', 0) * features.get('trend_strength', 0)
    if momentum_trend_product < 0:
        return "skip"
    return prediction