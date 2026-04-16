import streamlit as st
import pandas as pd
import plotly.express as px
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="GEHA D&A Culture Stock Market", layout="wide")

# --- INITIAL STATE MANAGEMENT ---
if 'facilitator_name' not in st.session_state:
    st.session_state.facilitator_name = ""
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

PHASES = [
    "Initial Allocation", 
    "Recognition Dividend", 
    "Strategic Pivot", 
    "Leadership Change", 
    "Open Enrollment & HEDIS", 
    "IT Build-a-Thon", 
    "Enterprise Project Kick-off",
    "Final Analysis"
]
current_phase = PHASES[st.session_state.phase]

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("Admin & Budget")
    
    st.session_state.facilitator_name = st.text_input(
        "Facilitator Name:", 
        value=st.session_state.facilitator_name,
        placeholder="e.g. Pablo Palmeri"
    )
    
    st.write(f"**Current Phase:** {current_phase}")
    st.divider()
    
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

    if st.button("🔄 Refresh Budget Alignment"):
        st.rerun()

    st.divider()

    if st.session_state.phase < len(PHASES) - 1:
        if is_balanced:
            if st.button("➡️ Advance to Next Phase"):
                snapshot = st.session_state.investments.copy()
                snapshot['Label'] = current_phase
                snapshot['Facilitator'] = st.session_state.facilitator_name
                st.session_state.history.append(snapshot)
                st.session_state.phase += 1
                st.rerun()
        else:
            st.button("➡️ Advance (Locked)", disabled=True)
    
    st.divider()

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

elif current_phase == "Recognition Dividend":
    st.header("✨ Early Event: Recognition Dividend")
    if 'recognition_applied' not in st.session_state:
        rec = st.session_state.investments["Recognition & Reinforcement"]
        if rec > 20:
            st.session_state.rec_msg = (f"DIVIDEND PAID: Recognition was ${rec}. Morale boost! Budget +$10.", "success")
            st.session_state.total_budget += 10
        else:
            st.session_state.rec_msg = (f"NO DIVIDEND: Recognition was only ${rec}.", "warning")
        st.session_state.recognition_applied = True
        st.rerun()
    
    msg, level = st.session_state.rec_msg
    if level == "success":
        st.success(msg)
    else:
        st.warning(msg)

elif current_phase == "Strategic Pivot":
    st.header("⚡ Market Event: Strategic Pivot")
    if 'pivot_applied' not in st.session_state:
        clarity = st.session_state.investments["Clarity & Decision Discipline"]
        if clarity < 20:
            st.session_state.pivot_msg = (f"FAILURE: Clarity was ${clarity}. Chaos ensued. Budget -$10.", "error")
            st.session_state.total_budget -= 10
        else:
            st.session_state.pivot_msg = (f"SUCCESS: Clarity was ${clarity}. Budget +$10.", "success")
            st.session_state.total_budget += 10
        st.session_state.pivot_applied = True
        st.rerun()
    
    msg, level = st.session_state.pivot_msg
    if level == "success":
        st.success(msg)
    else:
        st.error(msg)

elif current_phase == "Leadership Change":
    st.header("🚨 Market Event: Leadership Transition")
    if 'leadership_applied' not in st.session_state:
        safety = st.session_state.investments["Psychological Safety"]
        if safety < 20:
            st.session_state.leadership_msg = (f"FAILURE: Safety was ${safety}. You lose all ${safety} invested in Safety.", "error")
            st.session_state.total_budget -= safety
            st.session_state.investments["Psychological Safety"] = 0
            st.session_state.leadership_applied = True
            st.rerun()
        else:
            st.session_state.leadership_msg = (f"SUCCESS: Safety was ${safety}.", "success")
        st.session_state.leadership_applied = True
        st.rerun()
    
    msg, level = st.session_state.leadership_msg
    if level == "success":
        st.success(msg)
    else:
        st.error(msg)

elif current_phase == "Open Enrollment & HEDIS":
    st.header("❄️ Seasonal Event: Open Enrollment & HEDIS")
    if 'hedis_applied' not in st.session_state:
        pace = st.session_state.investments["Sustainable Pace & Focus"]
        if pace > 19:
            st.session_state.hedis_msg = (f"SUCCESS: Pace was ${pace}. Budget +$10.", "success")
            st.session_state.total_budget += 10
        else:
            st.session_state.hedis_msg = (f"FAILURE: Pace was ${pace}. Budget -$10.", "error")
            st.session_state.total_budget -= 10
        st.session_state.hedis_applied = True
        st.rerun()
    
    msg, level = st.session_state.hedis_msg
    if level == "success":
        st.success(msg)
    else:
        st.error(msg)

elif current_phase == "IT Build-a-Thon":
    st.header("🛠️ Event: IT Build-a-Thon")
    if 'buildathon_applied' not in st.session_state:
        team_score = st.session_state.investments["Cross-Team Partnership"]
        if team_score < 17:
            st.session_state.buildathon_msg = ("NO ENTRY.", "warning")
        elif 17 <= team_score <= 21:
            st.session_state.buildathon_msg = ("ENTRY AWARD: Budget +$5.", "success")
            st.session_state.total_budget += 5
        else:
            st.session_state.buildathon_msg = ("WINNER: Budget +$10.", "success")
            st.session_state.total_budget += 10
        st.session_state.buildathon_applied = True
        st.rerun()
    
    msg, level = st.session_state.buildathon_msg
    if level == "success":
        st.success(msg)
    else:
        st.warning(msg)

elif current_phase == "Enterprise Project Kick-off":
    st.header("🏢 Enterprise Project Kick-off")
    if 'enterprise_applied' not in st.session_state:
        partnership = st.session_state.investments["Cross-Team Partnership"]
        if partnership > 25:
            st.session_state.ent_msg = (f"SUCCESS: Partnership was ${partnership}. Budget +$20.", "success")
            st.session_state.total_budget += 20
        else:
            st.session_state.ent_msg = (f"MISSED: Partnership was ${partnership}.", "warning")
        st.session_state.enterprise_applied = True
        st.rerun()
    
    msg, level = st.session_state.ent_msg
    if level == "success":
        st.success(msg)
    else:
        st.warning(msg)

elif current_phase == "Final Analysis":
    st.header("📊 Final Market Analysis")
    
    if len(st.session_state.history) < 7:
        final_snap = st.session_state.investments.copy()
        final_snap['Label'] = "Final Outcome"
        final_snap['Facilitator'] = st.session_state.facilitator_name
        st.session_state.history.append(final_snap)
    
    hist_df = pd.DataFrame(st.session_state.history)
    plot_df = hist_df.melt(id_vars=['Label', 'Facilitator'], var_name='Behavior', value_name='Investment')
    
    fig = px.bar(plot_df, x='Behavior', y='Investment', color='Label', barmode='group', height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.facilitator_name:
        st.write(f"**Session facilitated by:** {st.session_state.facilitator_name}")

    st.divider()
    csv = hist_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f'culture_market_results_{st.session_state.facilitator_name.replace(" ", "_")}.csv',
        mime='text/csv',
    )

# --- LIVE CHART ---
if current_phase != "Final Analysis":
    st.divider()
    df = pd.DataFrame(list(st.session_state.investments.items()), columns=['Stock', 'Investment'])
    fig_live = px.bar(df, x='Stock', y='Investment', range_y=[0, 100], text_auto=True)
    st.plotly_chart(fig_live, use_container_width=True)
