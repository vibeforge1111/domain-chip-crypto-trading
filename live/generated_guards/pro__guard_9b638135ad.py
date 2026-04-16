def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Stochastic alignment
    if features.get("stoch_k", 50) < 30:
        bullish += 1
    elif features.get("stoch_k", 50) > 70:
        bearish += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish += 1
    
    # MACD histogram direction
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # RSI 2h broader context
    if features.get("rsi_2h", 50) < 35:
        bullish += 1
    elif features.get("rsi_2h", 50) > 65:
        bearish += 1
    
    # OBV slope momentum
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    elif features.get("obv_slope", 0) < 0:
        bearish += 1
    
    # BB position near edges
    bb_pos = features.get("bb_pct_b", 0.5)
    if bb_pos < 0.25:
        bullish += 1
    elif bb_pos > 0.75:
        bearish += 1
    
    # Require 2+ signals to confirm direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction