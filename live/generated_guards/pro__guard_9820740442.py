def guard(features: dict, prediction: str) -> str:
    """Reject trades when both Bollinger position and Stochastic confirm extreme overbought/oversold."""
    bb = features.get('bb_pct_b', 0.5)
    sk = features.get('stoch_k', 50)
    rsi2h = features.get('rsi_2h', 50)
    
    # Reject longs when overbought on multiple indicators
    if prediction == 'long' and bb > 0.9 and sk > 80 and rsi2h > 70:
        return 'skip'
    
    # Reject shorts when oversold on multiple indicators
    if prediction == 'short' and bb < 0.1 and sk < 20 and rsi2h < 30:
        return 'skip'
    
    return prediction