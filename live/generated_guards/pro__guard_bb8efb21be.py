def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    count = 0
    pred_dir = 1 if prediction == "long" else -1
    
    # RSI + Stochastic agreement
    if features['rsi_14'] < 30 and features['stoch_k'] < 20:
        count += 1
    elif features['rsi_14'] > 70 and features['stoch_k'] > 80:
        count += 1
    
    # VWAP deviation confirmation
    if pred_dir == 1 and features['vwap_deviation'] < -0.005:
        count += 1
    elif pred_dir == -1 and features['vwap_deviation'] > 0.005:
        count += 1
    
    # OBV + MACD agreement
    if features['obv_slope'] > 0 and features['macd_histogram'] > 0:
        count += 1
    elif features['obv_slope'] < 0 and features['macd_histogram'] < 0:
        count += 1
    
    # 2h RSI broader context
    if pred_dir == 1 and features['rsi_2h'] < 45:
        count += 1
    elif pred_dir == -1 and features['rsi_2h'] > 55:
        count += 1
    
    # Require 2+ signals to agree
    if count < 2:
        return "skip"
    
    return prediction