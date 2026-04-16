def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with momentum confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Long: near lower band (<10th percentile) + oversold stochastic
    if prediction == "long" and not (bb < 0.10 and stoch < 25):
        return "skip"
    
    # Short: near upper band (>90th percentile) + overbought stochastic
    if prediction == "short" and not (bb > 0.90 and stoch > 75):
        return "skip"
    
    return prediction