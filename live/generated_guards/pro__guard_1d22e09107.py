def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    # Reject longs when broader timeframe is bearish
    if prediction == 'long' and rsi_2h < 40:
        return 'skip'
    # Reject shorts when broader timeframe is bullish
    if prediction == 'short' and rsi_2h > 60:
        return 'skip'
    return prediction