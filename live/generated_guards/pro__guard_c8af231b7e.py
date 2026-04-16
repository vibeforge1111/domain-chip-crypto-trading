def guard(features: dict, prediction: str) -> str:
    """Guard using BB extremes and momentum confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    vwap = features.get('vwap_deviation', 0)
    
    # Long: near lower band OR oversold with VWAP confirmation
    if prediction == 'long' and (bb < 0.05 or (stoch < 25 and vwap < 0)):
        return prediction
    
    # Short: near upper band OR overbought with VWAP confirmation
    if prediction == 'short' and (bb > 0.95 or (stoch > 75 and vwap > 0)):
        return prediction
    
    return 'skip'