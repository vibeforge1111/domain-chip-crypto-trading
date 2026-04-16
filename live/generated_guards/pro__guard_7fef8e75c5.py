def guard(features: dict, prediction: str) -> str:
    """Filter signals during compression phases using BB position and momentum."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd_histogram = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect compression: price centered + aligned stochastic + weak momentum
    is_compression = (0.35 <= bb_pct_b <= 0.65 and 
                      abs(stoch_k - stoch_d) < 10 and 
                      abs(macd_histogram) < 0.001)
    
    if is_compression:
        # During compression, reject signals with strong VWAP deviation
        if abs(vwap_deviation) > 0.008:
            return "skip"
        # Reject if 2h RSI in extreme territory (likely reversal)
        if rsi_2h < 30 or rsi_2h > 70:
            return "skip"
    
    return prediction