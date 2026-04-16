def guard(features: dict, prediction: str) -> str:
    """Filter trades using bb_pct_b extremes with momentum confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    rsi = features.get('rsi_14', 50)
    macd = features.get('macd_histogram', 0)
    
    # High-confidence zones: bb_pct_b at extremes (<0.05 or >0.95)
    in_extreme_zone = bb < 0.05 or bb > 0.95
    
    if not in_extreme_zone:
        return "skip"
    
    # For long entries at lower extreme (<0.05), require bullish confirmation
    if prediction == "long" and bb < 0.05:
        if stoch < 20 and macd > 0:
            return prediction
        return "skip"
    
    # For short entries at upper extreme (>0.95), require bearish confirmation
    if prediction == "short" and bb > 0.95:
        if stoch > 80 and macd < 0:
            return prediction
        return "skip"
    
    return prediction