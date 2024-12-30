
#   Core Features
- **API Connectivity:**  
   - Seamlessly integrates with **Kraken's API** for **order execution** and **data retrieval**.
- **Sentiment Analysis:**  
   - Uses **pre-trained NLP models** (e.g., **FinBERT**) for **sentiment scoring**.
- **Technical Indicators:**  
   - Implements classic strategies such as **RSI** and **Moving Average**.
- **Risk Management:**  
   - Ensures **stop-loss**, **exposure limits**, and **position sizing** for controlled trading.
- **Backtesting:**  
   - Validate strategies using **historical data** to ensure performance before live trading.
- **Real-time Dashboard:**  
   - Monitor **portfolio metrics**, **live trades**, and **sentiment signals** via an interactive dashboard.
#  Future Focus
- **Advanced Machine Learning Models:**  
   - Implement **predictive analytics** using state-of-the-art ML algorithms.
- **Integration of Historical Markers:**  
   - Utilize **historical trading patterns** for smarter decision-making.
- **Dynamic Weighting Mechanisms:**  
   - Create **adaptive weighting systems** for sentiment and technical indicators.
- **Improved Backtesting Framework:**  
   - Enhance metrics like **Sharpe Ratio**, **Max Drawdown**, and **Win Rate**.
#   Libraries
**Language:** Python 3.x  
**API Integration:** Kraken REST API  
**Hosting Platform:** Render

**Key Libraries:**  
-  `pandas`, `numpy` → Data Handling  
-  `nltk`, `transformers`, `torch` → Sentiment Analysis  
-  `scikit-learn` → Machine Learning  
-  `flask`, `dash`, `plotly` → Dashboard & Visualization  
-  `backtrader` → Backtesting
  
## Requirements
To install all required dependencies, run:
```bash
pip install -r requirements.txt
```

## Set Environment Variables
```plaintext
KRAKEN_API_KEY = your_api_key
KRAKEN_PRIVATE_KEY = your_private_key
DEPLOYMENT_ENV = development
TRAINING_MODE = {mock, paper-trade, live}
```

## Run Bot Locally
```bash
python bot.py
```

## Launch Dashboard
```bash
cd modules/dashboard
python app.py
```
Access at: http://127.0.0.1:5000/



## Structure
```text
├── TradingBotXAI-main/
│   ├── README.md
│   ├── bot.py
│   ├── requirements.txt
│   ├── backtesting/
│   │   ├── __init__.py
│   │   ├── backtester.py
│   ├── config/
│   │   ├── config.py
│   │   ├── configuration.env
│   ├── dashboard/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── static/
│   │   │   ├── scripts.js
│   │   ├── templates/
│   │   │   ├── index.html
│   ├── data/
│   │   ├── mock_data_handler.py
│   │   ├── datasets/
│   │   │   ├── ADAUSD.csv
│   │   │   ├── Information.txt
│   │   │   ├── LTCUSD.csv
│   │   ├── live/
│   │   │   ├── current_data.json
│   │   │   ├── data_handler.py
│   │   ├── mock/
│   │   │   ├── mock_data.json
│   ├── execution/
│   │   ├── KrakenAPI.py
│   │   ├── __init__.py
│   │   ├── data_handler.py
│   │   ├── trade_executor.py
│   ├── ml/
│   │   ├── ML.py
│   │   ├── __init__.py
│   │   ├── ml_predictor.py
│   ├── portfolio/
│   │   ├── __init__.py
│   │   ├── portfolio.py
│   ├── risk/
│   │   ├── risk_manager.py

```



