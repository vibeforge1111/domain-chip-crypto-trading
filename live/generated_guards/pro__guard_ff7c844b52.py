def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree with direction."""
    
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Stochastic overbought/oversold
    if features.get('stoch_k', 50) < 20:
        bullish += 1
    elif features.get('stoch_k', 50) > 80:
        bearish += 1
    
    if features.get('stoch_d', 50) < 20:
        bullish += 1
    elif features.get('stoch_d', 50) > 80:
        bearish += 1
    
    # RSI 2h for broader context
    if features.get('rsi_2h', 50) < 35:
        bullish += 1
    elif features.get('rsi_2h', 50) > 65:
        bearish += 1
    
    # Bollinger Band position
    if features.get('bb_pct_b', 0.5) < 0.2:
        bullish += 1
    elif features.get('bb_pct_b', 0.5) > 0.8:
        bearish += 1
    
    # VWAP deviation from price
    if features.get('vwap_deviation', 0) < -0.005:
        bullish += 1
    elif features.get('vwap_deviation', 0) > 0.005:
        bearish += 1
    
    # OBV momentum direction
    if features.get('obv_slope', 0) > 0:
        bullish += 1
    elif features.get('obv_slope', 0) < 0:
        bearish += 1
    
    # MACD histogram direction
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish += 1
    
    # Require 2+ signals agreeing with direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction