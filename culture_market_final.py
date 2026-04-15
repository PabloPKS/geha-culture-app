import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="GEHA D&A Culture Stock Market", layout="wide", initial_sidebar_state="expanded")

# --- INITIAL STATE MANAGEMENT ---
if 'total_allowable_budget' not in st.session_state:
    st.session_state.total_allowable_budget = 100
if 'pivot_executed' not in st.session_state:
    st.session_state.pivot_executed = False
if 'history' not in st.session_state:
    # Track snapshots of the portfolio at key milestones
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

# --- HEADER ---
st.title("📈 GEHA D&A Culture Stock Market")
st.subheader("“Where Leaders Actually Invest”")

# --- SIDEBAR: PORTFOLIO MANAGEMENT ---
st.sidebar.header("Market Controls")

event_choice = st.sidebar.radio(
    "Active Phase:",
    ["Initial Allocation", "Strategic Pivot", "Leadership Change", "Final Review"],
    help="Move through the exercise phases in order."
)

# Persistent Budget Calculation
total_invested = sum(st.session_state.investments.values())
budget_diff = st.session_state.total_allowable_budget - total_invested

st.sidebar.metric("Current Budget Limit", f"${st.session_state.total_allowable_budget}")

if budget_diff < 0:
    st.sidebar.error(f"⚠️ OVER BUDGET: ${abs(budget_diff)}")
elif budget_diff > 0:
    st.sidebar.warning(f"Unallocated: ${budget_diff}")
else:
    st.sidebar.success("✅ Portfolio Balanced")

st.sidebar.divider()

# Only allow sliders if we aren't in the Final Review
if event_choice != "Final Review":
    for stock in st.session_state.investments.keys():
        st.session_state.investments[stock] = st.sidebar.slider(
            f"{stock}", 0, 100, st.session_state.investments[stock]
        )

# Snapshot Function
def save_snapshot(label):
    snapshot = st.session_state.investments.copy()
    snapshot['Label'] = label
    snapshot['Total Budget'] = st.session_state.total_allowable_budget
    # Prevent duplicate snapshots for the same label
    if not any(d['Label'] == label for d in st.session_state.history):
        st.session_state.history.append(snapshot)

# --- MAIN DASHBOARD ---
if event_choice == "Initial Allocation":
    st.write("### Phase 1: Establish Your Baseline")
    st.info("Allocate your initial $100. When finished, save the baseline to proceed.")
    if st.button("Save Baseline Portfolio"):
        save_snapshot("Initial Baseline")
        st.success("Baseline saved! Move to 'Strategic Pivot' in the sidebar.")

elif event_choice == "Strategic Pivot":
    st.header("⚡ Event: Strategic Change in Direction")
    if not st.session_state.pivot_executed:
        st.write("A sudden pivot in strategy has been announced. Your readiness depends on your Clarity.")
        if st.button("Calculate & Save Pivot Impact"):
            clarity = st.session_state.investments["Clarity & Decision Discipline"]
            if clarity > 25:
                st.session_state.total_allowable_budget += 10
                st.session_state.pivot_result = "SUCCESS (+10)"
            else:
                st.session_state.total_allowable_budget -= 10
                st.session_state.pivot_result = "FAIL (-10)"
            st.session_state.pivot_executed = True
            save_snapshot(f"Post-Pivot ({st.session_state.pivot_result})")
            st.rerun()
    else:
        st.write(f"**Result:** {st.session_state.pivot_result}. Your permanent budget is now ${st.session_state.total_allowable_budget}.")

elif event_choice == "Leadership Change":
    st.header("⚡ Event: The Leadership Pivot")
    st.error(f"MANDATE: A new leader demands immediate ROI visibility. Divest $10 from TWO areas and move $20 to Clarity.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        stocks_to_cut = [s for s in st.session_state.investments.keys() if s != "Clarity & Decision Discipline"]
        cut1 = st.selectbox("Sell $10 from:", stocks_to_cut, key="c1")
    with col_b:
        cut2 = st.selectbox("Sell $10 from:", [s for s in stocks_to_cut if s != cut1], key="c2")
    
    if st.button("Execute & Save Leadership Shift"):
        st.session_state.investments[cut1] -= 10
        st.session_state.investments[cut2] -= 10
        st.session_state.investments["Clarity & Decision Discipline"] += 20
        save_snapshot("Post-Leadership Change")
        st.success("Reallocation saved! Move to 'Final Review' to see the comparison.")

elif event_choice == "Final Review":
    st.header("📊 Final Market Analysis")
    if not st.session_state.history:
        st.warning("No snapshots saved. Please go back through the phases and click 'Save'.")
    else:
        # Prepare Data for Comparison
        comparison_df = pd.DataFrame(st.session_state.history)
        # Melt the dataframe for plotting
        plot_df = comparison_df.melt(id_vars=['Label', 'Total Budget'], var_name='Stock', value_name='Investment')
        # Remove 'Total Budget' from the Stock list if it slipped in
        plot_df = plot_df[plot_df['Stock'] != 'Total Budget']

        fig = px.bar(
            plot_df, 
            x='Stock', 
            y='Investment', 
            color='Label', 
            barmode='group',
            height=600,
            title="Portfolio Evolution: Start vs. End"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("### Cultural Shift Summary")
        for h in st.session_state.history:
            st.write(f"**{h['Label']}:** Total Budget ${h['Total Budget']} | Clarity: ${h['Clarity & Decision Discipline']} | Safety: ${h['Psychological Safety']}")

# Display Current Chart if not in Final Review
if event_choice != "Final Review":
    st.divider()
    df_current = pd.DataFrame(list(st.session_state.investments.items()), columns=['Stock', 'Investment'])
    fig_current = px.bar(df_current, x='Stock', y='Investment', range_y=[0, 100])
    st.plotly_chart(fig_current, use_container_width=True)
