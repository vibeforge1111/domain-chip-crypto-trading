def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions as high-confidence zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long' and not (bb_pct_b < 0.05 and rsi_2h < 40):
        return 'skip'
    if prediction == 'short' and not (bb_pct_b > 0.95 and rsi_2h > 60):
        return 'skip'
    return prediction