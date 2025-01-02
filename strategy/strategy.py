import pandas as pd
import numpy as np


class TechnicalStrategy:
    def __init__(self):
        self.data = pd.DataFrame()


       # 1. EMA (Exponential Moving Average)
    def ema_strategy(self, short_window: int = 12, long_window: int = 26) -> str:
        self.data['ema_short'] = self.data['close'].ewm(span=short_window).mean()
        self.data['ema_long'] = self.data['close'].ewm(span=long_window).mean()
        
        if self.data['ema_short'].iloc[-1] > self.data['ema_long'].iloc[-1]:
            return 'Buy'
        elif self.data['ema_short'].iloc[-1] < self.data['ema_long'].iloc[-1]:
            return 'Sell'
        return 'Hold'

    # 2. Parabolic SAR
    def parabolic_sar_strategy(self) -> str:
        self.data['psar'] = self.data['close'].shift(1) * 0.02
        if self.data['close'].iloc[-1] > self.data['psar'].iloc[-1]:
            return 'Buy'
        else:
            return 'Sell'

    # 3. Ichimoku Cloud
    def ichimoku_strategy(self) -> str:
        self.data['tenkan_sen'] = self.data['close'].rolling(window=9).mean()
        self.data['kijun_sen'] = self.data['close'].rolling(window=26).mean()
        self.data['senkou_span_a'] = ((self.data['tenkan_sen'] + self.data['kijun_sen']) / 2).shift(26)
        self.data['senkou_span_b'] = self.data['close'].rolling(window=52).mean().shift(26)
        
        if self.data['close'].iloc[-1] > self.data['senkou_span_a'].iloc[-1]:
            return 'Buy'
        elif self.data['close'].iloc[-1] < self.data['senkou_span_b'].iloc[-1]:
            return 'Sell'
        return 'Hold'

    # ===============================
    # MOMENTUM INDICATORS
    # ===============================
    # 4. Williams %R
    def williams_r_strategy(self, period: int = 14) -> str:
        self.data['williams_r'] = (self.data['high'].rolling(period).max() - self.data['close']) / (
            self.data['high'].rolling(period).max() - self.data['low'].rolling(period).min()) * -100
        
        if self.data['williams_r'].iloc[-1] > -20:
            return 'Sell'
        elif self.data['williams_r'].iloc[-1] < -80:
            return 'Buy'
        return 'Hold'

    # 5. Commodity Channel Index (CCI)
    def cci_strategy(self, period: int = 20) -> str:
        self.data['tp'] = (self.data['high'] + self.data['low'] + self.data['close']) / 3
        self.data['cci'] = (self.data['tp'] - self.data['tp'].rolling(window=period).mean()) / (
            0.015 * self.data['tp'].rolling(window=period).std())
        
        if self.data['cci'].iloc[-1] > 100:
            return 'Sell'
        elif self.data['cci'].iloc[-1] < -100:
            return 'Buy'
        return 'Hold'

    # 6. Momentum Indicator
    def momentum_strategy(self, period: int = 10) -> str:
        self.data['momentum'] = self.data['close'].diff(period)
        if self.data['momentum'].iloc[-1] > 0:
            return 'Buy'
        elif self.data['momentum'].iloc[-1] < 0:
            return 'Sell'
        return 'Hold'

    # ===============================
    # VOLATILITY INDICATORS
    # ===============================
    # 7. Keltner Channel
    def keltner_strategy(self) -> str:
        self.data['ema'] = self.data['close'].ewm(span=20).mean()
        self.data['atr'] = self.data['close'].diff().abs().rolling(window=14).mean()
        self.data['upper'] = self.data['ema'] + 2 * self.data['atr']
        self.data['lower'] = self.data['ema'] - 2 * self.data['atr']
        
        if self.data['close'].iloc[-1] > self.data['upper'].iloc[-1]:
            return 'Sell'
        elif self.data['close'].iloc[-1] < self.data['lower'].iloc[-1]:
            return 'Buy'
        return 'Hold'

    # 8. Donchian Channel
    def donchian_strategy(self, period: int = 20) -> str:
        self.data['upper'] = self.data['high'].rolling(window=period).max()
        self.data['lower'] = self.data['low'].rolling(window=period).min()
        
        if self.data['close'].iloc[-1] > self.data['upper'].iloc[-1]:
            return 'Buy'
        elif self.data['close'].iloc[-1] < self.data['lower'].iloc[-1]:
            return 'Sell'
        return 'Hold'

    # ===============================
    # SUPPORT/RESISTANCE
    # ===============================
    # 9. Pivot Points
    def pivot_points_strategy(self) -> str:
        self.data['pivot'] = (self.data['high'] + self.data['low'] + self.data['close']) / 3
        if self.data['close'].iloc[-1] > self.data['pivot'].iloc[-1]:
            return 'Buy'
        else:
            return 'Sell'

    # 10. Fibonacci Retracement
    def fibonacci_strategy(self) -> str:
        max_price = self.data['high'].max()
        min_price = self.data['low'].min()
        fib_level = min_price + (max_price - min_price) * 0.618
        if self.data['close'].iloc[-1] > fib_level:
            return 'Sell'
        else:
            return 'Buy'
      # ===============================
    def elliott_wave_strategy(self) -> str:
        """
        Identify Elliott Wave Patterns and make trading decisions.
        """
        if len(self.data) < 10:
            return 'Hold'  # Insufficient data
        
        # Simple wave pattern detection (placeholder logic)
        self.data['price_change'] = self.data['close'].diff()
        upward_moves = (self.data['price_change'] > 0).sum()
        downward_moves = (self.data['price_change'] < 0).sum()
        
        if upward_moves >= 5 and downward_moves >= 3:
            return 'Buy'  # Wave 3 detected
        elif downward_moves >= 5 and upward_moves >= 3:
            return 'Sell'  # Wave C detected
        else:
            return 'Hold'
    
    # ===============================
    # Wyckoff Strategy
    # ===============================
    def wyckoff_strategy(self) -> str:
        """
        Analyze Wyckoff patterns and determine market phase.
        """
        if len(self.data) < 20:
            return 'Hold'  # Insufficient data
        
        recent_lows = self.data['low'].rolling(window=5).min()
        recent_highs = self.data['high'].rolling(window=5).max()
        
        current_price = self.data['close'].iloc[-1]
        recent_low = recent_lows.iloc[-1]
        recent_high = recent_highs.iloc[-1]
        
        # Detect Wyckoff Accumulation and Distribution
        if current_price < recent_low * 1.05:
            return 'Buy'  # Potential Accumulation phase (Spring)
        elif current_price > recent_high * 0.95:
            return 'Sell'  # Potential Distribution phase (Upthrust)
        else:
            return 'Hold'
    
    # ===============================
    # Combined Strategy
    # ===============================
    def combined_strategy(self, pair: str) -> Dict[str, Any]:
        """
        Combine Elliott Wave, Wyckoff, and Technical Indicators.
        """
        elliott_signal = self.elliott_wave_strategy()
        wyckoff_signal = self.wyckoff_strategy()
        
        signals = [elliott_signal, wyckoff_signal]
        buy_signals = signals.count('Buy')
        sell_signals = signals.count('Sell')
        
        if buy_signals >= 2:
            return {'action': 'buy', 'reason': 'Elliott and Wyckoff alignment'}
        elif sell_signals >= 2:
            return {'action': 'sell', 'reason': 'Elliott and Wyckoff alignment'}
        else:
            return {'action': 'hold', 'reason': 'No strong alignment'}

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
    # Triple Moving Average Crossover 
    # ===============================
    def triple_ma_strategy(self, short_window: int = 5, medium_window: int = 15, long_window: int = 50) -> str:
        self.data['short_ma'] = self.data['close'].rolling(window=short_window).mean()
        self.data['medium_ma'] = self.data['close'].rolling(window=medium_window).mean()
        self.data['long_ma'] = self.data['close'].rolling(window=long_window).mean()
        
        if self.data['short_ma'].iloc[-1] > self.data['medium_ma'].iloc[-1] > self.data['long_ma'].iloc[-1]:
            return 'Buy'
        elif self.data['short_ma'].iloc[-1] < self.data['medium_ma'].iloc[-1] < self.data['long_ma'].iloc[-1]:
            return 'Sell'
        return 'Hold'

    # ===============================
    # Hull Moving Average (HMA)
    # ===============================
    def hma_strategy(self, period: int = 14) -> str:
        half_length = int(period / 2)
        sqrt_length = int(np.sqrt(period))
        
        self.data['hma'] = self.data['close'].rolling(half_length).mean() * 2 - self.data['close'].rolling(period).mean()
        self.data['hma'] = self.data['hma'].rolling(sqrt_length).mean()
        
        if self.data['hma'].iloc[-1] > self.data['hma'].iloc[-2]:
            return 'Buy'
        elif self.data['hma'].iloc[-1] < self.data['hma'].iloc[-2]:
            return 'Sell'
        return 'Hold'

    # ===============================
    # SuperTrend Indicator
    # ===============================   
    def supertrend_strategy(self, multiplier: float = 3, period: int = 14) -> str:
        hl2 = (self.data['high'] + self.data['low']) / 2
        atr = self.data['close'].diff().abs().rolling(window=period).mean()
        self.data['supertrend'] = hl2 + (multiplier * atr)
        
        if self.data['close'].iloc[-1] > self.data['supertrend'].iloc[-1]:
            return 'Buy'
        elif self.data['close'].iloc[-1] < self.data['supertrend'].iloc[-1]:
            return 'Sell'
        return 'Hold'

    # ===============================
    #  Rate of Change (ROC)
    # ===============================      
    def roc_strategy(self, period: int = 14) -> str:
        self.data['roc'] = self.data['close'].pct_change(period) * 100
        if self.data['roc'].iloc[-1] > 0:
            return 'Buy'
        elif self.data['roc'].iloc[-1] < 0:
            return 'Sell'
        return 'Hold'

    # ===============================
    # Moving Average Convergence Divergence Histogram (MACDH)
    # ===============================   
    def macd_histogram_strategy(self) -> str:
        self.data['ema12'] = self.data['close'].ewm(span=12).mean()
        self.data['ema26'] = self.data['close'].ewm(span=26).mean()
        self.data['macd'] = self.data['ema12'] - self.data['ema26']
        self.data['signal_line'] = self.data['macd'].ewm(span=9).mean()
        self.data['macd_histogram'] = self.data['macd'] - self.data['signal_line']
        
        if self.data['macd_histogram'].iloc[-1] > 0:
            return 'Buy'
        elif self.data['macd_histogram'].iloc[-1] < 0:
            return 'Sell'
        return 'Hold'


    # ===============================
    # Relative Vigor Index (RVI)
    # ===============================   
    def rvi_strategy(self, period: int = 10) -> str:
        self.data['rvi'] = ((self.data['close'] - self.data['open']) / (self.data['high'] - self.data['low'])).rolling(window=period).mean()
        if self.data['rvi'].iloc[-1] > 0:
            return 'Buy'
        elif self.data['rvi'].iloc[-1] < 0:
            return 'Sell'
        return 'Hold'


    # ===============================
    # Chaikin Volatility Indicator
    # ===============================       
    def chaikin_volatility_strategy(self, period: int = 10) -> str:
        self.data['volatility'] = (self.data['high'] - self.data['low']).rolling(window=period).mean()
        if self.data['volatility'].iloc[-1] > self.data['volatility'].iloc[-2]:
            return 'Sell'  # Market becoming unstable
        elif self.data['volatility'].iloc[-1] < self.data['volatility'].iloc[-2]:
            return 'Buy'  # Market stabilizing
        return 'Hold'

    # ===============================
    # Combine Strategies into Utility Score
    # ===============================
       def combined_strategy(self, pair: str) -> Dict[str, Any]:
        """
        Combine multiple technical indicators into a unified decision.
        """
        # Individual indicator signals
        rsi_signal = self.rsi_strategy(pair)
        ma_signal = self.ma_strategy(pair)
        macd_signal = self.macd_strategy()
        bollinger_signal = self.bollinger_strategy()
        stochastic_signal = self.stochastic_strategy()
        atr_value = self.atr_strategy()
        ema_signal = self.ema_strategy()
        parabolic_sar_signal = self.parabolic_sar_strategy()
        ichimoku_signal = self.ichimoku_strategy()
        williams_r_signal = self.williams_r_strategy()
        cci_signal = self.cci_strategy()
        momentum_signal = self.momentum_strategy()
        keltner_signal = self.keltner_strategy()
        donchian_signal = self.donchian_strategy()
        pivot_signal = self.pivot_points_strategy()
        fibonacci_signal = self.fibonacci_strategy()
        triple_ma_signal = self.triple_ma_strategy()
        hma_signal = self.hma_strategy()
        supertrend_signal = self.supertrend_strategy()
        roc_signal = self.roc_strategy()
        macd_histogram_signal = self.macd_histogram_strategy()
        rvi_signal = self.rvi_strategy()
        chaikin_volatility_signal = self.chaikin_volatility_strategy()
        mfi_signal = self.mfi_strategy()
        beta_signal = self.beta_strategy(market_returns=pd.Series(np.random.uniform(-0.05, 0.05, size=200)))

        # Map signals to numerical scores
        signal_mapping = {
            'Strong Buy': 2,
            'Buy': 1,
            'Hold': 0,
            'Sell': -1,
            'Strong Sell': -2}
        
        # Indicator weights (you can fine-tune these based on importance)
        indicator_weights = {
            'rsi': 0.1,
            'ma': 0.1,
            'macd': 0.1,
            'bollinger': 0.05,
            'stochastic': 0.05,
            'ema': 0.1,
            'parabolic_sar': 0.05,
            'ichimoku': 0.05,
            'williams_r': 0.05,
            'cci': 0.05,
            'momentum': 0.05,
            'keltner': 0.05,
            'donchian': 0.05,
            'pivot': 0.05,
            'fibonacci': 0.05,
            'triple_ma': 0.05,
            'hma': 0.05,
            'supertrend': 0.05,
            'roc': 0.05,
            'macd_histogram': 0.05,
            'rvi': 0.05,
            'chaikin_volatility': 0.05,
            'mfi': 0.05,
            'beta': 0.05}

        # Aggregate signals with weights
        weighted_score = sum([
            signal_mapping.get(rsi_signal, 0) * indicator_weights['rsi'],
            signal_mapping.get(ma_signal, 0) * indicator_weights['ma'],
            signal_mapping.get(macd_signal, 0) * indicator_weights['macd'],
            signal_mapping.get(bollinger_signal, 0) * indicator_weights['bollinger'],
            signal_mapping.get(stochastic_signal, 0) * indicator_weights['stochastic'],
            signal_mapping.get(ema_signal, 0) * indicator_weights['ema'],
            signal_mapping.get(parabolic_sar_signal, 0) * indicator_weights['parabolic_sar'],
            signal_mapping.get(ichimoku_signal, 0) * indicator_weights['ichimoku'],
            signal_mapping.get(williams_r_signal, 0) * indicator_weights['williams_r'],
            signal_mapping.get(cci_signal, 0) * indicator_weights['cci'],
            signal_mapping.get(momentum_signal, 0) * indicator_weights['momentum'],
            signal_mapping.get(keltner_signal, 0) * indicator_weights['keltner'],
            signal_mapping.get(donchian_signal, 0) * indicator_weights['donchian'],
            signal_mapping.get(pivot_signal, 0) * indicator_weights['pivot'],
            signal_mapping.get(fibonacci_signal, 0) * indicator_weights['fibonacci'],
            signal_mapping.get(triple_ma_signal, 0) * indicator_weights['triple_ma'],
            signal_mapping.get(hma_signal, 0) * indicator_weights['hma'],
            signal_mapping.get(supertrend_signal, 0) * indicator_weights['supertrend'],
            signal_mapping.get(roc_signal, 0) * indicator_weights['roc'],
            signal_mapping.get(macd_histogram_signal, 0) * indicator_weights['macd_histogram'],
            signal_mapping.get(rvi_signal, 0) * indicator_weights['rvi'],
            signal_mapping.get(chaikin_volatility_signal, 0) * indicator_weights['chaikin_volatility'],
            signal_mapping.get(mfi_signal, 0) * indicator_weights['mfi'],
            signal_mapping.get(beta_signal, 0) * indicator_weights['beta']])
        
        # Decision thresholds
        if weighted_score > 1.0:
            action = 'buy'
        elif weighted_score < -1.0:
            action = 'sell'
        else:
            action = 'hold'
        
        return {
            'action': action,
            'volatility': atr_value,
            'score': round(weighted_score, 2),
            'details': {
                'rsi': rsi_signal,
                'ma': ma_signal,
                'macd': macd_signal,
                'bollinger': bollinger_signal,
                'stochastic': stochastic_signal,
                'ema': ema_signal,
                'parabolic_sar': parabolic_sar_signal,
                'ichimoku': ichimoku_signal,
                'williams_r': williams_r_signal,
                'cci': cci_signal,
                'momentum': momentum_signal,
                'keltner': keltner_signal,
                'donchian': donchian_signal,
                'pivot': pivot_signal,
                'fibonacci': fibonacci_signal,
                'triple_ma': triple_ma_signal,
                'hma': hma_signal,
                'supertrend': supertrend_signal,
                'roc': roc_signal,
                'macd_histogram': macd_histogram_signal,
                'rvi': rvi_signal,
                'chaikin_volatility': chaikin_volatility_signal,
                'mfi': mfi_signal,
                'beta': beta_signal
            }
        }


# Example Usage
if __name__ == '__main__':
    strategy = TechnicalStrategy()
    strategy.data = pd.DataFrame({
        'close': np.random.uniform(50, 150, size=200),
        'high': np.random.uniform(150, 200, size=200),
        'low': np.random.uniform(40, 50, size=200),
        'open': np.random.uniform(50, 150, size=200),
        'volume': np.random.uniform(1000, 5000, size=200)
    })
    final_decision = strategy.combined_strategy('ADA/USD')
    print(f"[INFO] Final Trading Action: {final_decision}")
    })
    final_decision = strategy.combined_strategy('ADA/USD')
    print(f"[INFO] Final Trading Action: {final_decision}")
