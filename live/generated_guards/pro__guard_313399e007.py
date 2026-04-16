def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # RSI confirmation
    if features['rsi_14'] < 50:
        bullish += 1
    elif features['rsi_14'] > 50:
        bearish += 1
    
    # MACD momentum confirmation
    if features['macd_histogram'] > 0:
        bullish += 1
    elif features['macd_histogram'] < 0:
        bearish += 1
    
    # OBV trend confirmation
    if features['obv_slope'] > 0:
        bullish += 1
    elif features['obv_slope'] < 0:
        bearish += 1
    
    # VWAP position confirmation
    if features['vwap_deviation'] > 0:
        bullish += 1
    elif features['vwap_deviation'] < 0:
        bearish += 1
    
    # Bollinger position confirmation
    if features['bb_pct_b'] < 0.5:
        bullish += 1
    elif features['bb_pct_b'] > 0.5:
        bearish += 1
    
    # Stochastic confirmation
    if features['stoch_k'] > 50:
        bullish += 1
    elif features['stoch_k'] < 50:
        bearish += 1
    
    # Require 2+ signals to agree with direction
    if prediction == "long" and bullish < 2:
        return "skip"
    elif prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction