def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long when broader trend is bearish (rsi_2h very low)
    if prediction == 'long' and rsi_2h < 38:
        return 'skip'
    
    # Skip short when broader trend is bullish (rsi_2h very high)
    if prediction == 'short' and rsi_2h > 62:
        return 'skip'
    
    return prediction