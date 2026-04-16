def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    long_confirm = 0
    short_confirm = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) < 35:
        long_confirm += 1
    elif features.get('rsi_14', 50) > 65:
        short_confirm += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 20:
        long_confirm += 1
    elif features.get('stoch_k', 50) > 80:
        short_confirm += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) > 0.002:
        long_confirm += 1
    elif features.get('vwap_deviation', 0) < -0.002:
        short_confirm += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        long_confirm += 1
    elif features.get('obv_slope', 0) < 0:
        short_confirm += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        long_confirm += 1
    elif features.get('macd_histogram', 0) < 0:
        short_confirm += 1
    
    # Bollinger Band position confirmation
    if features.get('bb_pct_b', 0.5) < 0.25:
        long_confirm += 1
    elif features.get('bb_pct_b', 0.5) > 0.75:
        short_confirm += 1
    
    # Require 2+ indicators to agree
    if prediction == "long" and long_confirm >= 2:
        return prediction
    elif prediction == "short" and short_confirm >= 2:
        return prediction
    
    return "skip"