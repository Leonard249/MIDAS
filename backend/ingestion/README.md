# Moomoo API Data Ingestion Catalog

This catalog documents all candidate endpoints available via the Moomoo API for ingestion into `midas_market_data.duckdb`. These data points serve as foundational inputs for downstream Quant (feature engineering & signal modeling) and NLP (sentiment scoring & temporal alignment) modules in the MIDAS platform.

---

## 1. Market & Technical Price Data

- **Get Historical Candlesticks**: Retrieves past Open, High, Low, Close, and Volume (OHLCV) time-series across daily and intraday timeframes (K_DAY, K_5M, K_1M).
- **Get Adjustment Factor**: Returns forward and backward split/dividend multipliers (AuType.QFQ) required to construct continuous price charts without split-induced distortions.
- **Get Market Status of Securities**: Tracks real-time session states indicating regular market hours, pre-market, after-hours, or trading halts.
- **Get Capital Flow**: Provides net cash inflow/outflow metrics segmented by transaction scale (small, medium, large, and extra-large block orders).
- **Get Capital Distribution**: Captures volume concentration across pending bid and ask levels within the order book.
- **Get Plates of Stocks**: Maps securities to industry, sector, and thematic concept groups for cross-sectional analysis and universe sorting.
- **Get Top Ten Buy/Sell Brokers**: Tracks order volume routed by major brokerages and market makers to analyze institutional order flow.

---

## 2. Fundamental & Financial Data

- **Get Financial Statements**: Ingests structured line items directly from Income Statements, Balance Sheets, and Statements of Cash Flows.
- **Get Revenue Breakdown**: Segments historical revenue streams across specific product lines, business units, and geographic regions.
- **Get Valuation Detail**: Tracks daily and quarterly valuation metrics, including P/E, P/B, P/S, and EV/EBITDA ratios over time.
- **Get Valuation Plate Stock List**: Sector-wide valuation benchmarks for comparative peer valuation models.
- **Get Company Operational Efficiency**: Ingests operational management KPIs, such as Return on Equity (ROE), Return on Assets (ROA), and inventory turnover ratios.

---

## 3. Corporate Actions

- **Get Corporate Actions - Dividends**: Ingests announcement dates, ex-dividend dates, payout amounts, and dividend yield metrics.
- **Get Corporate Actions - Buybacks**: Tracks share repurchase program authorizations, execution volume, and corporate buyback schedules.
- **Get Corporate Actions - Stock Splits**: Details historical forward and reverse stock split ratios alongside official execution dates.

---

## 4. Analyst Research & Earnings Impact

- **Get Earnings Price Move**: Measures historical percentage price swings and realized volatility in the immediate aftermath of earnings releases.
- **Get Earnings Price History**: Tracks actual vs. estimated Earnings Per Share (EPS) and revenue surprises alongside stock price reaction curves.
- **Get Research Analyst Consensus**: Aggregates Wall Street consensus ratings (Buy/Hold/Sell) and target price probability distributions.
- **Get Research Rating Summary**: Detailed breakdown of analyst upgrades, downgrades, and target price revisions over time.
- **Get Morningstar Research Report**: Ingests quantitative and qualitative research ratings provided by Morningstar analysts.

---

## 5. Ownership & Insider Activity

- **Get Shareholders Overview**: Tracks overall equity ownership structure broken down by institutions, corporate insiders, and public float.
- **Get Shareholders Holding Changes**: Ingests quarter-over-quarter position adjustments by major institutional managers (13F filings tracking).
- **Get Shareholders Holder Detail**: Identifies top institutional shareholders and their exact position sizing.
- **Get Institutional Holdings**: Aggregate share count and portfolio weighting held across institutional funds.
- **Get Insider Holder List**: Lists total equity ownership held by company officers, directors, and major insiders.
- **Get Insider Trade List**: Ingests Form 4 open-market buy and sell transactions executed by corporate insiders.

---

## 6. Short Selling Metrics

- **Get Daily Short Volume**: Daily aggregate short selling volume relative to total daily trading volume.
- **Get Short Interest**: Tracks total shares sold short, short float percentages, and days-to-cover ratios for short-squeeze signal feature engineering.

---

## 7. Company Metadata

- **Get Company Profile**: Core company metadata, sector/industry classifications, corporate headquarters location, and business summaries.
- **Get Company Executives**: Directory of C-suite officers, key managers, and board members.
- **Get Company Executive Background**: Professional biographies, prior corporate tenure, and executive management histories.
