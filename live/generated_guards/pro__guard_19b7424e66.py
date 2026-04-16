def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == 'skip':
        return prediction
    
    bullish = 0
    bearish = 0
    
    # RSI 2h context confirmation
    if features['rsi_2h'] > 50:
        bullish += 1
    else:
        bearish += 1
    
    # Stochastic confirmation (away from extremes)
    if features['stoch_k'] < 75:
        bullish += 1
    if features['stoch_k'] > 25:
        bearish += 1
    
    # VWAP deviation confirmation
    if features['vwap_deviation'] > 0:
        bullish += 1
    if features['vwap_deviation'] < 0:
        bearish += 1
    
    # MACD histogram confirmation
    if features['macd_histogram'] > 0:
        bullish += 1
    if features['macd_histogram'] < 0:
        bearish += 1
    
    # OBV slope confirmation
    if features['obv_slope'] > 0:
        bullish += 1
    if features['obv_slope'] < 0:
        bearish += 1
    
    # BB position confirmation
    if features['bb_pct_b'] > 0.5:
        bullish += 1
    if features['bb_pct_b'] < 0.5:
        bearish += 1
    
    # Require 2+ confirmations aligned with direction
    if prediction == 'long' and bullish >= 2:
        return prediction
    if prediction == 'short' and bearish >= 2:
        return prediction
    
    return 'skip'