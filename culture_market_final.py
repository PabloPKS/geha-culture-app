import streamlit as st
import pandas as pd
import plotly.express as px

# --- PERSISTENT STATE ---
if 'phase_index' not in st.session_state:
    st.session_state.phase_index = 0
if 'total_allowable_budget' not in st.session_state:
    st.session_state.total_allowable_budget = 100
if 'history' not in st.session_state:
    st.session_state.history = []
if 'investments' not in st.session_state:
    st.session_state.investments = {
        "Psychological Safety": 15,
        "Cross-Team Partnership": 15,
        "Clarity & Decision Discipline": 15,
        "Healthy Debate": 15,
        "Recognition & Reinforcement": 15,
        "Sustainable Pace & Focus": 15
    }

phases = ["Initial Allocation", "Strategic Pivot", "Leadership Change", "Final Analysis"]
current_phase = phases[st.session_state.phase_index]

# --- UI HEADER ---
st.title("📈 GEHA D&A Culture Stock Market")
st.subheader(f"Current Phase: {current_phase}")

# --- BUDGET MONITORING ---
total_invested = sum(st.session_state.investments.values())
budget_diff = st.session_state.total_allowable_budget - total_invested

# --- SIDEBAR (ONLY SLIDERS) ---
with st.sidebar:
    st.header("Portfolio Management")
    st.metric("Total Budget", f"${st.session_state.total_allowable_budget}")
    
    # Sliders are disabled during the Final Analysis
    if current_phase != "Final Analysis":
        for stock in st.session_state.investments.keys():
            st.session_state.investments[stock] = st.sidebar.slider(
                f"{stock}", 0, 100, st.session_state.investments[stock]
            )

# --- PHASE LOGIC ---

if current_phase == "Initial Allocation":
    st.info("Allocate your initial $100 across the behaviors below.")
    if st.button("Lock Portfolio & Close Markets"):
        # Save snapshot
        snapshot = st.session_state.investments.copy()
        snapshot['Label'] = "Initial Baseline"
        st.session_state.history.append(snapshot)
        # Advance Phase
        st.session_state.phase_index += 1
        st.rerun()

elif current_phase == "Strategic Pivot":
    st.warning("⚠️ MARKET ALERT: Strategic Change in Direction")
    st.write("A sudden pivot has been announced. We are checking your 'Clarity & Decision Discipline' levels...")
    
    if st.button("Calculate Impact"):
        clarity = st.session_state.investments["Clarity & Decision Discipline"]
        if clarity > 25:
            st.session_state.total_allowable_budget += 10
            res = "Success (+10)"
        else:
            st.session_state.total_allowable_budget -= 10
            res = "Fail (-10)"
        
        # Save snapshot
        snapshot = st.session_state.investments.copy()
        snapshot['Label'] = f"Post-Pivot ({res})"
        st.session_state.history.append(snapshot)
        st.session_state.phase_index += 1
        st.rerun()

elif current_phase == "Leadership Change":
    st.error("🚨 CRISIS: The Leadership Pivot")
    st.write("New leadership demands visibility. You must divest $10 from TWO stocks and move $20 to Clarity.")
    
    # Reallocation logic tools here...
    # [Insert selectbox logic from previous version]
    
    if st.button("Execute & Finalize"):
        # Logic to apply cuts...
        snapshot = st.session_state.investments.copy()
        snapshot['Label'] = "Final Result"
        st.session_state.history.append(snapshot)
        st.session_state.phase_index += 1
        st.rerun()

elif current_phase == "Final Analysis":
    st.header("📊 The Cultural Cost of Business")
    # Comparison Chart logic...
