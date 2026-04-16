def guard(features: dict, prediction: str) -> str:
    """Filter trades in low-volatility, neutral-momentum conditions (choppy market)."""
    # Reject when ATR is very low (choppy) AND RSI is neutral (no clear direction)
    if features.get('atr_ratio', 1.0) < 0.5 and 40 < features.get('rsi_14', 50) < 60:
        return "skip"
    return prediction