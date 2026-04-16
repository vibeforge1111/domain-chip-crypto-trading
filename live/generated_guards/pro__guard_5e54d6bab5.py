def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover alignment."""
    sk, sd = features["stoch_k"], features["stoch_d"]
    
    # For longs: require bullish crossover (k above d) and not overbought
    if prediction == "long" and (sk <= sd or sk > 80):
        return "skip"
    
    # For shorts: require bearish crossover (k below d) and not oversold
    if prediction == "short" and (sk >= sd or sk < 20):
        return "skip"
    
    return prediction