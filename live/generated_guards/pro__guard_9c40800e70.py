def guard(features: dict, prediction: str) -> str:
    """Filter trades where candle range is unusually tight relative to ATR."""
    if features.get('range_pct', 0) < features.get('atr_ratio', 1) * 0.5:
        return "skip"
    return prediction