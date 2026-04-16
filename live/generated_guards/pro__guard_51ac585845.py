def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic bullish (not overbought)
    if features.get('stoch_k', 50) > features.get('stoch_d', 50) and features.get('stoch_k', 100) < 80:
        confirmations += 1
    
    # VWAP deviation bullish (above VWAP)
    if features.get('vwap_deviation', 0) > 0:
        confirmations += 1
    
    # OBV slope bullish
    if features.get('obv_slope', 0) > 0:
        confirmations += 1
    
    # MACD histogram bullish
    if features.get('macd_histogram', 0) > 0:
        confirmations += 1
    
    # RSI confirmation (not overbought/oversold)
    if 35 <= features.get('rsi_14', 50) <= 65:
        confirmations += 1
    
    # BB position in middle range
    if 0.25 <= features.get('bb_pct_b', 0.5) <= 0.75:
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction