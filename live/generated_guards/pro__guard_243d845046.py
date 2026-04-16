def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return "skip"
    
    bullish_signals = 0
    bearish_signals = 0
    
    # Stochastic: bounce from oversold or rejection from overbought
    if features.get('stoch_k', 50) < 30 and features.get('stoch_d', 50) < 30:
        bullish_signals += 1
    elif features.get('stoch_k', 50) > 70 and features.get('stoch_d', 50) > 70:
        bearish_signals += 1
    
    # Bollinger position: near lower band = bullish, upper = bearish
    if features.get('bb_pct_b', 0.5) < 0.2:
        bullish_signals += 1
    elif features.get('bb_pct_b', 0.5) > 0.8:
        bearish_signals += 1
    
    # VWAP: price above = bullish, below = bearish
    if features.get('vwap_deviation', 0) > 0:
        bullish_signals += 1
    elif features.get('vwap_deviation', 0) < 0:
        bearish_signals += 1
    
    # RSI 2h: strength confirmation
    if features.get('rsi_2h', 50) > 55:
        bullish_signals += 1
    elif features.get('rsi_2h', 50) < 45:
        bearish_signals += 1
    
    # OBV slope: accumulation/distribution
    if features.get('obv_slope', 0) > 0:
        bullish_signals += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_signals += 1
    
    # MACD histogram: momentum direction
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_signals += 1
    
    # Require at least 2 confirming signals
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    elif prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction