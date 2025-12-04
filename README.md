# Options Arbitrage Dashboard

Interactive Streamlit app for checking basic no‑arbitrage conditions on European call and put options and visualizing payoffs for common spreads.

---

## Overview

The app lets you input strikes and call/put prices, then:

- Check standard no‑arbitrage inequalities for vertical and butterfly spreads  
- Flag potential arbitrage opportunities (e.g. overpriced legs)  
- Generate payoff tables for each strategy  
- Plot payoff diagrams across underlying prices for the identified structures  

This project was built as a learning tool for derivatives pricing and arbitrage

---

## Tech stack

- Python  
- Streamlit  
- NumPy  
- Matplotlib (or Plotly, if you switched)  

---

## Getting started

1.Clone the repository:

git clone https://github.com/your-username/options-arbitrage-dashboard.git
cd options-arbitrage-dashboard

2.Create and activate a virtual environment (optional but recommended), then install dependencies:

pip install -r requirements.txt

3.Run the app:

streamlit run arb_app.py


---

## How to use

1. Select the option type mode (calls, puts, or both).  
2. Enter strikes \(X_1, X_2, X_3\) and corresponding option prices.  
3. Click **Run checks** to compute flags, payoff tables, and payoff diagrams.  
4. Review:
   - Flags for any detected arbitrage  
   - Payoff tables for each strategy  
   - Payoff charts to see the profit profile at expiry  

---

## Arbitrage logic

The checks are based on standard no‑arbitrage relationships between option prices, such as:

- Monotonicity and convexity of call/put prices across strikes  
- Bounds on vertical spread prices  
- Butterfly spreads having non‑negative prices under no arbitrage  

These conditions are implemented in the core functions used by the dashboard, which return flags that drive the tables and plots.
