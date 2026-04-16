def guard(features: dict, prediction: str) -> str:
    """Skip trades when macd_histogram shows momentum deceleration against direction."""
    if prediction == "skip":
        return prediction
    
    macd = features.get("macd_histogram", 0)
    obv = features.get("obv_slope", 0)
    
    # Skip long if momentum weakening (neg macd) AND volume diverging (neg obv)
    if prediction == "long" and macd < -0.0002 and obv < 0:
        return "skip"
    
    # Skip short if momentum strengthening (pos macd) AND volume diverging (pos obv)
    if prediction == "short" and macd > 0.0002 and obv > 0:
        return "skip"
    
    return prediction