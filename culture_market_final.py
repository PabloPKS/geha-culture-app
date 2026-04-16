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
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = ""
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

# --- AI ANALYSIS FUNCTION (Simulated) ---
def get_ai_analysis(data):
    # This logic mimics an AI's evaluation of the specific numbers
    safety = data["Psychological Safety"]
    partnership = data["Cross-Team Partnership"]
    clarity = data["Clarity & Decision Discipline"]
    pace = data["Sustainable Pace & Focus"]
    
    analysis = ""
    if safety < 10 and clarity > 30:
        analysis = "This culture operates as a high-precision but high-fear engine, where technical clarity is prioritized over the human safety required to report errors. While efficient in the short term, the 'silence tax' creates a massive hidden risk for catastrophic project failure under pressure."
    elif partnership > 30 and pace < 15:
        analysis = "Your team excels at breaking down silos and winning enterprise projects through sheer collaborative force. However, the dangerously low investment in sustainable pace suggests this success is built on a foundation of imminent burnout that will eventually erode your partnership gains."
    elif safety > 25 and clarity > 25:
        analysis = "This is a rare 'High-Trust, High-Clarity' culture where teams are empowered to move fast because they know exactly where they are going and feel safe enough to course-correct. You have built a resilient operating model that can likely withstand significant leadership turnover without losing its soul."
    else:
        analysis = f"This portfolio shows a pragmatic but reactive culture that prioritizes the most immediate business pressures. While you managed to capture specific event bonuses, the lack of a dominant 'cultural anchor' suggests the team may struggle to maintain its identity during the next major organizational shift."
    
    return analysis

# --- SIDEBAR ---
with st.sidebar:
    st.title("Admin & Budget")
    st.session_state.facilitator_name = st.text_input("Facilitator Name:", value=st.session_state.facilitator_name)
    st.write(f"**Phase:** {current_phase}")
    st.metric("Target Budget", f"${st.session_state.total_budget}")
    
    total_spent = sum(st.session_state.investments.values())
    diff = st.session_state.total_budget - total_spent
    is_balanced = (diff == 0)

    if diff < 0: st.error(f"⚠️ OVER BUDGET: ${abs(diff)}")
    elif diff > 0: st.warning(f"Unallocated: ${diff}")
    else: st.success("✅ Portfolio Balanced")

    if st.button("🔄 Refresh"): st.rerun()
    st.divider()

    if st.session_state.phase < len(PHASES) - 1:
        if is_balanced:
            if st.button("➡️ Advance Phase"):
                snapshot = st.session_state.investments.copy()
                snapshot['Label'] = current_phase
                st.session_state.history.append(snapshot)
                st.session_state.phase += 1
                st.rerun()
        else:
            st.button("➡️ Advance (Locked)", disabled=True)

    if current_phase != "Final Analysis":
        for stock in st.session_state.investments.keys():
            st.session_state.investments[stock] = st.number_input(f"{stock}", min_value=0, max_value=200, value=int(st.session_state.investments[stock]), key=f"in_{stock}")

# --- MAIN DASHBOARD ---
st.title("📈 GEHA D&A Culture Stock Market")

# [Logic for Events 1-7 (Implicitly the same as v10)]
if current_phase == "Initial Allocation":
    st.info("Teams: Distribute your $100. Advance button unlocks when budget is balanced.")
elif current_phase == "Recognition Dividend":
    if 'recognition_applied' not in st.session_state:
        rec = st.session_state.investments["Recognition & Reinforcement"]
        if rec > 20: st.session_state.total_budget += 10; st.session_state.rec_res = ("SUCCESS: Morale boost! +$10", "success")
        else: st.session_state.rec_res = ("NO DIVIDEND: Low recognition.", "warning")
        st.session_state.recognition_applied = True; st.rerun()
    msg, lvl = st.session_state.rec_res
    st.success(msg) if lvl=="success" else st.warning(msg)
elif current_phase == "Strategic Pivot":
    if 'pivot_applied' not in st.session_state:
        if st.session_state.investments["Clarity & Decision Discipline"] < 20: st.session_state.total_budget -= 10; st.session_state.piv_res = ("FAIL: Clarity too low. -$10", "error")
        else: st.session_state.total_budget += 10; st.session_state.piv_res = ("SUCCESS: Clarity payed off! +$10", "success")
        st.session_state.pivot_applied = True; st.rerun()
    msg, lvl = st.session_state.piv_res
    st.success(msg) if lvl=="success" else st.error(msg)
elif current_phase == "Leadership Change":
    if 'leadership_applied' not in st.session_state:
        safety = st.session_state.investments["Psychological Safety"]
        if safety < 20: st.session_state.total_budget -= safety; st.session_state.investments["Psychological Safety"] = 0; st.session_state.ldr_res = (f"FAIL: Safety lost (${safety})", "error")
        else: st.session_state.ldr_res = ("SUCCESS: Safety held.", "success")
        st.session_state.leadership_applied = True; st.rerun()
    msg, lvl = st.session_state.ldr_res
    st.success(msg) if lvl=="success" else st.error(msg)
elif current_phase == "Open Enrollment & HEDIS":
    if 'hedis_applied' not in st.session_state:
        if st.session_state.investments["Sustainable Pace & Focus"] > 19: st.session_state.total_budget += 10; st.session_state.hed_res = ("SUCCESS: Pace held. +$10", "success")
        else: st.session_state.total_budget -= 10; st.session_state.hed_res = ("FAIL: Burnout. -$10", "error")
        st.session_state.hedis_applied = True; st.rerun()
    msg, lvl = st.session_state.hed_res
    st.success(msg) if lvl=="success" else st.error(msg)
elif current_phase == "IT Build-a-Thon":
    if 'buildathon_applied' not in st.session_state:
        pts = st.session_state.investments["Cross-Team Partnership"]
        if pts < 17: st.session_state.bld_res = ("NO ENTRY.", "warning")
        elif pts <= 21: st.session_state.total_budget += 5; st.session_state.bld_res = ("ENTRY: +$5", "success")
        else: st.session_state.total_budget += 10; st.session_state.bld_res = ("WINNER: +$10", "success")
        st.session_state.buildathon_applied = True; st.rerun()
    msg, lvl = st.session_state.bld_res
    st.success(msg) if lvl=="success" else st.warning(msg)
elif current_phase == "Enterprise Project Kick-off":
    if 'enterprise_applied' not in st.session_state:
        if st.session_state.investments["Cross-Team Partnership"] > 25: st.session_state.total_budget += 20; st.session_state.ent_res = ("SUCCESS: +$20", "success")
        else: st.session_state.ent_res = ("MISSED BONUS.", "warning")
        st.session_state.enterprise_applied = True; st.rerun()
    msg, lvl = st.session_state.ent_res
    st.success(msg) if lvl=="success" else st.warning(msg)

elif current_phase == "Final Analysis":
    st.header("📊 Final Market Analysis")
    
    # Save final snap
    if len(st.session_state.history) < 7:
        final_snap = st.session_state.investments.copy()
        final_snap['Label'] = "Final Outcome"
        st.session_state.history.append(final_snap)
    
    hist_df = pd.DataFrame(st.session_state.history)
    plot_df = hist_df.melt(id_vars=['Label'], var_name='Behavior', value_name='Investment')
    fig = px.bar(plot_df, x='Behavior', y='Investment', color='Label', barmode='group', height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.subheader("🤖 AI Executive Cultural Summary")
    if st.button("Analyze Cultural DNA"):
        with st.spinner("AI evaluating priorities..."):
            st.session_state.ai_summary = get_ai_analysis(st.session_state.investments)
    
    if st.session_state.ai_summary:
        st.markdown(f"**{st.session_state.ai_summary}**")
    
    st.divider()
    csv = hist_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results (CSV)", data=csv, file_name=f'geha_results_{st.session_state.facilitator_name}.csv', mime='text/csv')

if current_phase != "Final Analysis":
    st.divider()
    df = pd.DataFrame(list(st.session_state.investments.items()), columns=['Stock', 'Investment'])
    fig_live = px.bar(df, x='Stock', y='Investment', range_y=[0, 100], text_auto=True)
    st.plotly_chart(fig_live, use_container_width=True)
