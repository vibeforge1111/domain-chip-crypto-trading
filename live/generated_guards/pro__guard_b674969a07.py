def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    long_confirm = 0
    short_confirm = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) < 70:
        long_confirm += 1
    if features.get('rsi_14', 50) > 30:
        short_confirm += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 80:
        long_confirm += 1
    if features.get('stoch_k', 50) > 20:
        short_confirm += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        long_confirm += 1
    if features.get('macd_histogram', 0) < 0:
        short_confirm += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        long_confirm += 1
    if features.get('obv_slope', 0) < 0:
        short_confirm += 1
    
    # Require 2+ confirmations for valid signal
    if prediction == "long" and long_confirm < 2:
        return "skip"
    if prediction == "short" and short_confirm < 2:
        return "skip"
    
    return prediction