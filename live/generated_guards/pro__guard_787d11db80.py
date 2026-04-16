def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like bb_pct_b, stoch_k, stoch_d, vwap_deviation, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip when both Bollinger position AND Stochastic confirm extreme overbought/oversold
    if bb_pct > 0.9 and stoch_k > 80:
        return "skip"
    if bb_pct < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction