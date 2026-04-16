def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Get confirmation signals
    vwap_aligned = features.get('vwap_deviation', 0) > 0 if prediction == "long" else features.get('vwap_deviation', 0) < 0
    stoch_aligned = features.get('stoch_k', 50) < 70 if prediction == "long" else features.get('stoch_k', 50) > 30
    obv_aligned = features.get('obv_slope', 0) > 0 if prediction == "long" else features.get('obv_slope', 0) < 0
    macd_aligned = features.get('macd_histogram', 0) > 0 if prediction == "long" else features.get('macd_histogram', 0) < 0
    
    confirmations = sum([vwap_aligned, stoch_aligned, obv_aligned, macd_aligned])
    
    return "skip" if confirmations < 2 else prediction