import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from arb_core import check_arbitrage, payoff_table, vertical_call_payoff, vertical_put_payoff, butterfly_call_payoff, butterfly_put_payoff, payoff_table_butterfly

st.set_page_config(layout="wide")
st.title("Options Arbitrage Dashboard")


mode_label = st.radio(
    "Option type",
    ["Calls only", "Puts only", "Both calls and puts"],
    index=0,
)
mode = {"Calls only": "c", "Puts only" : "p", "Both calls and puts": "b"}[mode_label]
# 1. Inputs
X1 = st.number_input("Strike X1", value=0)
X2 = st.number_input("Strike X2", value=0)
X3 = st.number_input("Strike X3", value=0)

if mode in ("c", "b"):
    st.subheader("Call prices")
    cx1 = st.number_input("Call price at X1", value=0)
    cx2 = st.number_input("Call price at X2", value=0)
    cx3 = st.number_input("Call price at X3", value=0)
else:
    cx1 = cx2 = cx3 = None

if mode in ("p", "b"):
    st.subheader("Put prices")
    px1 = st.number_input("Put price at X1", value=0)
    px2 = st.number_input("Put price at X2", value=0)
    px3 = st.number_input("Put price at X3", value=0)
else:
    px1 = px2 = px3 = None

inputs = {
    "mode": mode,
    "X1": X1, "X2": X2, "X3": X3,
    "Cx1": cx1, "Cx2": cx2, "Cx3": cx3,
    "Px1": px1, "Px2": px2, "Px3": px3,
}

if st.button("Run checks"):
    flags = check_arbitrage(inputs)
    st.write("Flags:", flags)

    table = payoff_table(inputs, flags)
    btfly_table = payoff_table_butterfly(inputs, flags)

    blocks = []

    if 'cx2_overpriced' in flags or 'cx1_overpriced' in flags:
        which = 'cx2_overpriced' if 'cx2_overpriced' in flags else 'cx1_overpriced'
        S = np.linspace(0.5*X1, 1.5*X3, 300)
        y = vertical_call_payoff(S, X1, X2, cx1, cx2, which)

        def render_vertical_call(container):
            container.subheader('Vertical Call Payoff')
            container.dataframe(table)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=S, y=y, mode='lines', name='Arbitrage Payoff', line=dict(width=3, color='darkblue')))
            fig.update_layout(title='Vertical Call Arbitrage', xaxis_title='Stock Price', yaxis_title='Payoff', width=800, height=500, showlegend=True, grid=dict(rows=1, columns=1))
            container.plotly_chart(fig, use_container_width=True)

        blocks.append(render_vertical_call)

    
    if 'butterfly' in flags:
        S_b = np.linspace(0.5*X1, 1.5*X3, 300)
        y_b = butterfly_call_payoff(S, X1, X2, X3, cx1, cx2, cx3)

        def render_bfly_call(container):
            container.subheader('Call Butterfly Payoff')
            container.dataframe(btfly_table)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=S_b, y=y_b, mode='lines', name='Arbitrage Payoff', line=dict(width=3, color='darkblue')))
            fig.update_layout(title='Butterfly Arbitrage', xaxis_title='Stock Price', yaxis_title='Payoff', width=800, height=500, showlegend=True, grid=dict(rows=1, columns=1))
            container.plotly_chart(fig, use_container_width=True)

        blocks.append(render_bfly_call)


    if 'px1_overpriced' in flags or 'px2_overpriced' in flags:
        which = 'px1_overpriced' if 'px1_overpriced' in flags else 'px2_overpriced'
        S_p = np.linspace(0.5*X1, 1.5*X3, 300)
        y_p = vertical_put_payoff(S, X1, X2, px1, px2, which)

        def render_vertical_put(container):
            container.subheader('Vertical Put Payoff')
            container.dataframe(table)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=S_p, y=y_p, mode='lines', name='Arbitrage Payoff', line=dict(width=3, color='darkblue')))
            fig.update_layout(title='Vertical Call Arbitrage', xaxis_title='Stock Price', yaxis_title='Payoff', width=800, height=500, showlegend=True, grid=dict(rows=1, columns=1))
            container.plotly_chart(fig, use_container_width=True)
        
        blocks.append(render_vertical_put)


    if 'butterlfy_put' in flags:
        S_pb = np.linspace(0.5*X1, 1.5*X3, 300)
        y_pb = butterfly_put_payoff(S, X1, X2, X3, px1, px2, px3)

        def render_bfly_put(container):
            container.subheader('Put Butterfly Payoff')
            container.dataframe(btfly_table)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=S_pb, y=y_pb, mode='lines', name='Arbitrage Payoff', line=dict(width=3, color='darkblue')))
            fig.update_layout(title='Butterfly Arbitrage', xaxis_title='Stock Price', yaxis_title='Payoff', width=800, height=500, showlegend=True, grid=dict(rows=1, columns=1))
            container.plotly_chart(fig, use_container_width=True)
        
        blocks.append(render_bfly_put)
        

    col1, col2 = st.columns(2)

    for i, render in enumerate(blocks):
        container = col1 if i % 2 == 0 else col2
        render(container)

        
        
        
        

