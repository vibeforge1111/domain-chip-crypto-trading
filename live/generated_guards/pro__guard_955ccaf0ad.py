def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard - requires 2+ signals to align."""
    if prediction == "skip":
        return "skip"
    
    confirmations = 0
    
    # RSI confirmation (not in extreme zone)
    if 35 < features.get("rsi_14", 50) < 65:
        confirmations += 1
    
    # Stochastic confirmation (not overbought/oversold)
    if 25 < features.get("stoch_k", 50) < 75:
        confirmations += 1
    
    # VWAP confirmation (price near or beyond VWAP in direction of trade)
    vwap = features.get("vwap_deviation", 0)
    if (prediction == "long" and vwap > -0.005) or (prediction == "short" and vwap < 0.005):
        confirmations += 1
    
    # MACD confirmation (histogram aligns with direction)
    if (prediction == "long" and features.get("macd_histogram", 0) > 0) or \
       (prediction == "short" and features.get("macd_histogram", 0) < 0):
        confirmations += 1
    
    # OBV slope confirmation (volume accumulation in direction)
    if (prediction == "long" and features.get("obv_slope", 0) > 0) or \
       (prediction == "short" and features.get("obv_slope", 0) < 0):
        confirmations += 1
    
    # BB position confirmation (not at extreme band)
    bb = features.get("bb_pct_b", 0.5)
    if 0.2 < bb < 0.8:
        confirmations += 1
    
    # Require 2+ indicators to confirm before allowing trade
    if confirmations >= 2:
        return prediction
    return "skip"