def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes."""
    bb = features.get('bb_pct_b', 0.5)
    vwap = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    
    # Only accept trades at BB extremes (<0.05 or >0.95)
    if bb < 0.05 or bb > 0.95:
        if prediction == "long" and (stoch < 20 or vwap < 0):
            return "skip"
        if prediction == "short" and (stoch > 80 or vwap > 0):
            return "skip"
    
    return prediction