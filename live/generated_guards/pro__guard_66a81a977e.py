def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions as high-confidence entry zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # High-confidence entry zones: bb_pct_b < 0.05 or > 0.95
    if bb_pct_b < 0.05:
        # Lower band extreme: valid for longs only, require oversold confirmation
        if prediction == "long" and stoch_k < 25:
            return prediction
        return "skip"
    elif bb_pct_b > 0.95:
        # Upper band extreme: valid for shorts only, require overbought confirmation
        if prediction == "short" and stoch_k > 75:
            return prediction
        return "skip"
    
    # Not at extreme BB zone - skip for high confidence
    return "skip"