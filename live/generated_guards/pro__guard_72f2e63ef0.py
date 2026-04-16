def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish confirmations
    bullish = sum([
        features.get('bb_pct_b', 0.5) > 0.5,
        features.get('vwap_deviation', 0) > 0.001,
        features.get('obv_slope', 0) > 0,
        features.get('macd_histogram', 0) > 0,
        features.get('rsi_2h', 50) > 50
    ])
    
    # Count bearish confirmations
    bearish = sum([
        features.get('bb_pct_b', 0.5) < 0.5,
        features.get('vwap_deviation', 0) < -0.001,
        features.get('obv_slope', 0) < 0,
        features.get('macd_histogram', 0) < 0,
        features.get('rsi_2h', 50) < 50
    ])
    
    # Require 2+ indicators to confirm the direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction