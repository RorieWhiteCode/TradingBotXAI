import pandas as pd
import numpy as np


class TechnicalStrategy:
    def __init__(self):
        self.data = pd.DataFrame()
    
    # ===============================
    # RSI Strategy
    # ===============================
    def rsi_strategy(self, pair: str, period: int = 14) -> str:
        self.data['rsi'] = self.calculate_rsi(self.data['close'], period)
        current_rsi = self.data['rsi'].iloc[-1]
        if current_rsi < 30:
            return 'Strong Buy'
        elif current_rsi < 50:
            return 'Buy'
        elif current_rsi > 70:
            return 'Strong Sell'
        else:
            return 'Hold'
    
    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    # ===============================
    # Moving Average Crossover Strategy
    # ===============================
    def ma_strategy(self, pair: str, short_window: int = 50, long_window: int = 200) -> str:
        self.data['short_ma'] = self.data['close'].rolling(window=short_window).mean()
        self.data['long_ma'] = self.data['close'].rolling(window=long_window).mean()
        
        if self.data['short_ma'].iloc[-1] > self.data['long_ma'].iloc[-1]:
            return 'Buy'
        elif self.data['short_ma'].iloc[-1] < self.data['long_ma'].iloc[-1]:
            return 'Sell'
        else:
            return 'Hold'
    
    # ===============================
    # MACD Strategy
    # ===============================
    def macd_strategy(self) -> str:
        self.data['ema12'] = self.data['close'].ewm(span=12).mean()
        self.data['ema26'] = self.data['close'].ewm(span=26).mean()
        self.data['macd'] = self.data['ema12'] - self.data['ema26']
        self.data['signal_line'] = self.data['macd'].ewm(span=9).mean()
        
        if self.data['macd'].iloc[-1] > self.data['signal_line'].iloc[-1]:
            return 'Buy'
        elif self.data['macd'].iloc[-1] < self.data['signal_line'].iloc[-1]:
            return 'Sell'
        else:
            return 'Hold'
    
    # ===============================
    # Bollinger Bands Strategy
    # ===============================
    def bollinger_strategy(self) -> str:
        self.data['rolling_mean'] = self.data['close'].rolling(window=20).mean()
        self.data['rolling_std'] = self.data['close'].rolling(window=20).std()
        self.data['upper_band'] = self.data['rolling_mean'] + (2 * self.data['rolling_std'])
        self.data['lower_band'] = self.data['rolling_mean'] - (2 * self.data['rolling_std'])
        
        current_price = self.data['close'].iloc[-1]
        
        if current_price > self.data['upper_band'].iloc[-1]:
            return 'Sell'
        elif current_price < self.data['lower_band'].iloc[-1]:
            return 'Buy'
        else:
            return 'Hold'
    
    # ===============================
    # Stochastic Oscillator Strategy
    # ===============================
    def stochastic_strategy(self, period: int = 14) -> str:
        self.data['lowest_low'] = self.data['low'].rolling(window=period).min()
        self.data['highest_high'] = self.data['high'].rolling(window=period).max()
        self.data['%K'] = (self.data['close'] - self.data['lowest_low']) / (self.data['highest_high'] - self.data['lowest_low']) * 100
        
        if self.data['%K'].iloc[-1] < 20:
            return 'Buy'
        elif self.data['%K'].iloc[-1] > 80:
            return 'Sell'
        else:
            return 'Hold'
    
    # ===============================
    # Average True Range (ATR) Strategy
    # ===============================
    def atr_strategy(self, period: int = 14) -> float:
        self.data['high_low'] = self.data['high'] - self.data['low']
        self.data['high_close'] = abs(self.data['high'] - self.data['close'].shift())
        self.data['low_close'] = abs(self.data['low'] - self.data['close'].shift())
        self.data['true_range'] = self.data[['high_low', 'high_close', 'low_close']].max(axis=1)
        self.data['atr'] = self.data['true_range'].rolling(window=period).mean()
        
        return self.data['atr'].iloc[-1]
    
    # ===============================
    # Combine Strategies into Utility Score
    # ===============================
    def combined_strategy(self, pair: str) -> Dict[str, Any]:
        rsi_signal = self.rsi_strategy(pair)
        ma_signal = self.ma_strategy(pair)
        macd_signal = self.macd_strategy()
        bollinger_signal = self.bollinger_strategy()
        stochastic_signal = self.stochastic_strategy()
        atr_value = self.atr_strategy()
        
        signals = [rsi_signal, ma_signal, macd_signal, bollinger_signal, stochastic_signal]
        signal_score = sum([1 if s == 'Buy' else -1 if s == 'Sell' else 0 for s in signals])
        
        return {
            'action': 'buy' if signal_score > 2 else 'sell' if signal_score < -2 else 'hold',
            'volatility': atr_value
        }


# Example Usage
if __name__ == '__main__':
    strategy = TechnicalStrategy()
    strategy.data = pd.DataFrame({
        'close': np.random.uniform(50, 150, size=200),
        'high': np.random.uniform(150, 200, size=200),
        'low': np.random.uniform(40, 50, size=200)
    })
    final_decision = strategy.combined_strategy('ADA/USD')
    print(f"[INFO] Final Trading Action: {final_decision}")
