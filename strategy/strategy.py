import asyncio
from typing import Dict, Any
from sentiment.collector import SentimentCollector
from sentiment.processor import SentimentPreprocessor
from sentiment.model import SentimentAnalyzer
from sentiment.aggregator import SentimentAggregator
from sentiment.signal import SignalGenerator
import pandas as pd
import numpy as np


# Technical Strategy Class (Expanded)
class TechnicalStrategy:
    def __init__(self):
        self.data = pd.DataFrame()
    
    # Calculate RSI
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
    
    # Calculate Moving Average Crossover
    def ma_strategy(self, pair: str, short_window: int = 50, long_window: int = 200) -> str:
        self.data['short_ma'] = self.data['close'].rolling(window=short_window).mean()
        self.data['long_ma'] = self.data['close'].rolling(window=long_window).mean()
        
        if self.data['short_ma'].iloc[-1] > self.data['long_ma'].iloc[-1]:
            return 'Buy'
        elif self.data['short_ma'].iloc[-1] < self.data['long_ma'].iloc[-1]:
            return 'Sell'
        else:
            return 'Hold'
    
    # Helper Function for RSI
    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))


# Combined Strategy with Sentiment Integration
class TradingStrategy:
    def __init__(self):
        self.technical_strategy = TechnicalStrategy()
        self.sentiment_collector = SentimentCollector()
        self.sentiment_preprocessor = SentimentPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.sentiment_aggregator = SentimentAggregator()
        self.signal_generator = SignalGenerator()
        
        # Weights for signal combination
        self.weights = {
            'technical': 0.6,
            'sentiment': 0.4
        }

    # Fetch Sentiment Signal
    async def fetch_sentiment_signal(self) -> Dict[str, Any]:
        try:
            await self.sentiment_collector.fetch_all_data()
            raw_sentiment_data = self.sentiment_collector.get_data()
            preprocessed_data = self.sentiment_preprocessor.preprocess_all(raw_sentiment_data)
            sentiment_results = self.sentiment_analyzer.batch_analyze(preprocessed_data)
            aggregated_sentiment = self.sentiment_aggregator.aggregate_sentiment(sentiment_results)
            sentiment_signal = self.signal_generator.generate_signal(aggregated_sentiment)
            return sentiment_signal
        except Exception as e:
            print(f"[ERROR] Failed to fetch sentiment signal: {e}")
            return {'signal': 'Hold', 'trade_size': 0.0}

    # Combine Technical and Sentiment Signals
    def combine_signals(self, technical_signal: str, sentiment_signal: Dict[str, Any]) -> Dict[str, Any]:
        signal_mapping = {
            'Strong Buy': 1.0,
            'Buy': 0.5,
            'Hold': 0.0,
            'Sell': -0.5,
            'Strong Sell': -1.0
        }
        
        technical_score = signal_mapping.get(technical_signal, 0.0)
        sentiment_score = signal_mapping.get(sentiment_signal.get('signal', 'Hold'), 0.0)
        
        combined_score = (
            (technical_score * self.weights['technical']) +
            (sentiment_score * self.weights['sentiment'])
        )
        
        if combined_score >= 0.7:
            return {'action': 'buy', 'trade_size': sentiment_signal.get('trade_size', 0.0)}
        elif combined_score <= -0.7:
            return {'action': 'sell', 'trade_size': sentiment_signal.get('trade_size', 0.0)}
        else:
            return {'action': 'hold', 'trade_size': 0.0}

    # Main Strategy Execution
    async def execute_strategy(self, pair: str):
        print(f"[INFO] Executing strategy for {pair}...")
        
        # Mock data for testing
        self.technical_strategy.data = pd.DataFrame({
            'close': np.random.uniform(50, 150, size=200)
        })
        
        # Fetch Technical Signal
        technical_signal = self.technical_strategy.rsi_strategy(pair)
        print(f"[INFO] Technical Signal: {technical_signal}")
        
        # Fetch Sentiment Signal
        sentiment_signal = await self.fetch_sentiment_signal()
        print(f"[INFO] Sentiment Signal: {sentiment_signal['signal']}")
        
        # Combine Signals
        final_decision = self.combine_signals(technical_signal, sentiment_signal)
        print(f"[INFO] Final Decision: {final_decision}")
        
        return final_decision


# Example Usage
if __name__ == '__main__':
    import asyncio

    strategy = TradingStrategy()
    pair = 'ADA/USD'
    final_decision = asyncio.run(strategy.execute_strategy(pair))
    print(f"[INFO] Final Trading Action: {final_decision}")

