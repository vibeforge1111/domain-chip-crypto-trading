def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic confirmation (oversold/bullish when < 30, overbought/bearish when > 70)
    if features.get('stoch_k', 50) < 30:
        bullish_count += 1
    elif features.get('stoch_k', 50) > 70:
        bearish_count += 1
    
    # Stochastic trend (K above D in lower half = bullish, K below D in upper half = bearish)
    if features.get('stoch_k', 50) > features.get('stoch_d', 50) and features.get('stoch_k', 50) < 50:
        bullish_count += 1
    elif features.get('stoch_k', 50) < features.get('stoch_d', 50) and features.get('stoch_k', 50) > 50:
        bearish_count += 1
    
    # VWAP deviation (above VWAP = bullish, below = bearish)
    if features.get('vwap_deviation', 0) > 0.005:
        bullish_count += 1
    elif features.get('vwap_deviation', 0) < -0.005:
        bearish_count += 1
    
    # BB position (lower band = bullish, upper band = bearish)
    if features.get('bb_pct_b', 0.5) < 0.2:
        bullish_count += 1
    elif features.get('bb_pct_b', 0.5) > 0.8:
        bearish_count += 1
    
    # OBV slope momentum
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # MACD histogram direction
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # Require 2+ confirming signals for the trade direction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    elif prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction