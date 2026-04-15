import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="GEHA D&A Culture Stock Market", layout="wide")

# --- INITIAL STATE MANAGEMENT ---
if 'total_budget' not in st.session_state:
    st.session_state.total_budget = 100
if 'history' not in st.session_state:
    st.session_state.history = []
if 'phase' not in st.session_state:
    st.session_state.phase = 0
if 'investments' not in st.session_state:
    st.session_state.investments = {
        "Psychological Safety": 0,
        "Cross-Team Partnership": 0,
        "Clarity & Decision Discipline": 0,
        "Healthy Debate": 0,
        "Recognition & Reinforcement": 0,
        "Sustainable Pace & Focus": 0
    }

PHASES = ["Initial Allocation", "Strategic Pivot", "Leadership Change", "Open Enrollment & HEDIS", "IT Build-a-Thon", "Final Analysis"]
current_phase = PHASES[st.session_state.phase]

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("Admin & Budget")
    st.write(f"**Phase:** {current_phase}")
    
    # 1. BUDGET CALCULATION
    st.metric("Target Budget", f"${st.session_state.total_budget}")
    total_spent = sum(st.session_state.investments.values())
    diff = st.session_state.total_budget - total_spent
    
    is_balanced = (diff == 0)

    if diff < 0:
        st.error(f"⚠️ OVER BUDGET: ${abs(diff)}")
    elif diff > 0:
        st.warning(f"Unallocated: ${diff}")
    else:
        st.success("✅ Portfolio Balanced")

    # 2. REFRESH BUTTON
    if st.button("🔄 Refresh Budget Alignment"):
        st.rerun()

    st.divider()

    # 3. ADVANCE PHASE
    if st.session_state.phase < len(PHASES) - 1:
        if is_balanced:
            if st.button("➡️ Advance to Next Phase"):
                snapshot = st.session_state.investments.copy()
                snapshot['Label'] = current_phase
                st.session_state.history.append(snapshot)
                st.session_state.phase += 1
                st.rerun()
        else:
            st.button("➡️ Advance (Locked)", disabled=True, help="You must balance the budget to proceed.")
    
    st.divider()

    # 4. NUMERIC INPUT BOXES
    if current_phase != "Final Analysis":
        st.write("### Enter Investments ($)")
        for stock in st.session_state.investments.keys():
            st.session_state.investments[stock] = st.number_input(
                f"{stock}", 
                min_value=0, 
                max_value=200, 
                value=int(st.session_state.investments[stock]),
                step=1,
                key=f"input_{stock}"
            )

# --- MAIN DASHBOARD ---
st.title("📈 GEHA D&A Culture Stock Market")

if current_phase == "Initial Allocation":
    st.header("Phase 1: Your Cultural Baseline")
    st.info("Teams: Enter dollar amounts. Advance button unlocks when budget is exactly $100.")

elif current_phase == "Strategic Pivot":
    st.header("⚡ Market Event: Strategic Pivot")
    if 'pivot_applied' not in st.session_state:
        clarity = st.session_state.investments["Clarity & Decision Discipline"]
        if clarity < 20:
            st.session_state.pivot_msg = (f"FAILURE: Clarity score is ${clarity} (Min: $20). Budget -$10.", "error")
            st.session_state.total_budget -= 10
        else:
            st.session_state.pivot_msg = (f"SUCCESS: Clarity score is ${clarity}. Budget +$10.", "success")
            st.session_state.total_budget += 10
        st.session_state.pivot_applied = True
    msg, level = st.session_state.pivot_msg
    if level == "success": st.success(msg)
    else: st.error(msg)
    st.write("Adjust your inputs to proceed.")

elif current_phase == "Leadership Change":
    st.header("🚨 Market Event: Leadership Transition")
    if 'leadership_applied' not in st.session_state:
        safety = st.session_state.investments["Psychological Safety"]
        if safety < 20:
            loss = safety
            st.session_state.leadership_msg = (f"FAILURE: Psych Safety was ${safety} (Min: $20). You lose all ${loss} invested in Safety.", "error")
            st.session_state.total_budget -= loss
            st.session_state.investments["Psychological Safety"] = 0
            st.session_state.leadership_applied = True
            st.rerun()
        else:
            st.session_state.leadership_msg = (f"SUCCESS: Psych Safety was ${safety}. Your team was safe enough to lead through the transition.", "success")
        st.session_state.leadership_applied = True
    msg, level = st.session_state.leadership_msg
    if level == "success": st.success(msg)
    else: st.error(msg)

elif current_phase == "Open Enrollment & HEDIS":
    st.header("❄️ Seasonal Event: Open Enrollment & HEDIS Season")
    st.info("The time of year where extra effort is key. Your resilience depends on your Pace & Focus.")
    if 'hedis_applied' not in st.session_state:
        pace = st.session_state.investments["Sustainable Pace & Focus"]
        if pace > 19:
            st.session_state.hedis_msg = (f"SUCCESS: Sustainable Pace was ${pace} (Threshold: >$19). The team had the reserve to meet objectives! Budget +$10.", "success")
            st.session_state.total_budget += 10
        else:
            st.session_state.hedis_msg = (f"FAILURE: Sustainable Pace was only ${pace}. Burnout during HEDIS resulted in errors and missed objectives. Budget -$10.", "error")
            st.session_state.total_budget -= 10
        st.session_state.hedis_applied = True
        st.rerun()
    msg, level = st.session_state.hedis_msg
    if level == "success": st.success(msg)
    else: st.error(msg)

elif current_phase == "IT Build-a-Thon":
    st.header("🛠️ Event: IT Build-a-Thon")
    st.write("Innovation time! If your team is too lean, you can't participate.")
    if 'buildathon_applied' not in st.session_state:
        # Assuming we check Cross-Team Partnership for this innovation event
        team_score = st.session_state.investments["Cross-Team Partnership"]
        if team_score < 17:
            st.session_state.buildathon_msg = (f"NO ENTRY: Your Team Partnership score is ${team_score}. You didn't have the collaborative capacity to enter. $0 reward.", "warning")
        elif 17 <= team_score <= 21:
            st.session_state.buildathon_msg = (f"ENTRY AWARD: Team Partnership score is ${team_score}. You successfully entered and collaborated. Budget +$5.", "success")
            st.session_state.total_budget += 5
        else:
            st.session_state.buildathon_msg = (f"WINNER: Team Partnership score is ${team_score}. High collaboration led to a Build-a-Thon victory! Budget +$10.", "success")
            st.session_state.total_budget += 10
        st.session_state.buildathon_applied = True
        st.rerun()
    msg, level = st.session_state.buildathon_msg
    if level == "success": st.success(msg)
    elif level == "warning": st.warning(msg)
    else: st.error(msg)

elif current_phase == "Final Analysis":
    st.header("📊 The Final Audit: Intent vs. Reality")
    if len(st.session_state.history) < 5:
        final_snap = st.session_state.investments.copy()
        final_snap['Label'] = "Final Outcome"
        st.session_state.history.append(final_snap)
    hist_df = pd.DataFrame(st.session_state.history)
    plot_df = hist_df.melt(id_vars=['Label'], var_name='Behavior', value_name='Investment')
    fig = px.bar(plot_df, x='Behavior', y='Investment', color='Label', barmode='group', height=600)
    st.plotly_chart(fig, use_container_width=True)

# --- LIVE CHART ---
if current_phase != "Final Analysis":
    st.divider()
    df = pd.DataFrame(list(st.session_state.investments.items()), columns=['Stock', 'Investment'])
    fig_live = px.bar(df, x='Stock', y='Investment', range_y=[0, 100], text_auto=True)
    st.plotly_chart(fig_live, use_container_width=True)
