# Options-Arbitrage-Dashboard

Interactive Streamlit app for checking basic no‑arbitrage conditions on European call and put options and visualizing payoffs for common spreads.

Overview
The app lets you input strikes and call/put prices, then:

Checks standard no‑arbitrage inequalities for vertical and butterfly spreads.

Flags potential arbitrage opportunities (e.g. overpriced legs).

Generates payoff tables for each strategy.

Plots payoff diagrams across underlying prices for the identified structures.

This project was built as a learning tool for derivatives pricing and arbitrage, and as a small options analytics dashboard for CV/portfolio use.

Tech stack
Python

Streamlit

NumPy

Matplotlib (or Plotly, if you switched)

Getting started
Clone the repository:

bash
git clone https://github.com/your-username/options-arbitrage-dashboard.git
cd options-arbitrage-dashboard
Create and activate a virtual environment (optional but recommended).

Install dependencies:

bash
pip install -r requirements.txt
Run the app:

bash
streamlit run arb_app.py
How to use
Select the option type mode (calls, puts, or both).

Enter strikes 
X
1
,
X
2
,
X
3
X 
1
 ,X 
2
 ,X 
3
  and corresponding option prices.

Click Run checks to compute flags, payoff tables, and payoff diagrams.

Review:

Flags for any detected arbitrage.

Payoff tables for each strategy.

Payoff charts to see the profit profile at expiry.

Arbitrage logic (high level)
The checks are based on standard no‑arbitrage relationships between option prices, such as:

Monotonicity and convexity of call/put prices across strikes.

Vertical spread bounds.

Butterfly spreads having non‑negative prices under no arbitrage.

These conditions are implemented in arb_core.py (or equivalent), which returns flags that drive the tables and plots.
