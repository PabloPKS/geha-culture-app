import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="GEHA D&A Culture Stock Market", layout="wide")

# --- INITIAL STATE ---
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
        "Psychological Safety": 0, "Cross-Team Partnership": 0,
        "Clarity & Decision Discipline": 0, "Healthy Debate": 0,
        "Recognition & Reinforcement": 0, "Sustainable Pace & Focus": 0
    }

PHASES = ["Initial Allocation", "Recognition Dividend", "Strategic Pivot", "Leadership Change", "Open Enrollment & HEDIS", "IT Build-a-Thon", "Enterprise Project Kick-off", "Final Analysis"]
current_phase = PHASES[st.session_state.phase]

# --- SIDEBAR & BUDGET LOGIC ---
with st.sidebar:
    st.title("Admin & Budget")
    st.session_state.facilitator_name = st.text_input("Facilitator Name:", value=st.session_state.facilitator_name)
    st.metric("Target Budget", f"${st.session_state.total_budget}")
    
    total_spent = sum(st.session_state.investments.values())
    diff = st.session_state.total_budget - total_spent
    
    if diff < 0: st.error(f"⚠️ OVER BUDGET: ${abs(diff)}")
    elif diff > 0: st.warning(f"Unallocated: ${diff}")
    else: st.success("✅ Portfolio Balanced")

    if st.button("🔄 Refresh"): st.rerun()

    if st.session_state.phase < len(PHASES) - 1:
        if diff == 0:
            if st.button("➡️ Advance Phase"):
                snap = st.session_state.investments.copy()
                snap['Label'] = current_phase
                st.session_state.history.append(snap)
                st.session_state.phase += 1
                st.rerun()
        else:
            st.button("➡️ Advance (Locked)", disabled=True)

    if current_phase != "Final Analysis":
        for stock in st.session_state.investments.keys():
            st.session_state.investments[stock] = st.number_input(f"{stock}", min_value=0, max_value=200, value=int(st.session_state.investments[stock]), key=f"in_{stock}")

# --- MAIN DASHBOARD ---
st.title("📈 GEHA D&A Culture Stock Market")

# PHASE 1: INITIAL
if current_phase == "Initial Allocation":
    st.info("**STAGE: Cultural Baseline**\n\n**Criteria:** Distribute exactly $100 across the six cultural behaviors.\n\n**Why it matters:** This represents your current 'default' operating model. Culture isn't what we say; it's what we pay for with our time and focus.")

# PHASE 2: RECOGNITION
elif current_phase == "Recognition Dividend":
    st.info("**STAGE: Recognition Dividend**\n\n**Success Criteria:** Recognition > $20. \n**Failure Criteria:** Recognition <= $20.\n\n**Why it matters:** High-recognition cultures create a 'positive attitude' multiplier. Without it, the team performs their duties but lacks the discretionary effort that drives extra productivity.")
    if 'rec_app' not in st.session_state:
        val = st.session_state.investments["Recognition & Reinforcement"]
        if val > 20: st.session_state.total_budget += 10; st.session_state.rec_res = ("SUCCESS: Morale boost! +$10", "success")
        else: st.session_state.rec_res = ("NO DIVIDEND: Low recognition.", "warning")
        st.session_state.rec_app = True; st.rerun()
    msg, lvl = st.session_state.rec_res
    if lvl == "success": st.success(msg)
    else: st.warning(msg)

# PHASE 3: PIVOT
elif current_phase == "Strategic Pivot":
    st.info("**STAGE: Strategic Pivot**\n\n**Success Criteria:** Clarity >= $20. \n**Failure Criteria:** Clarity < $20.\n\n**Why it matters:** When strategy shifts, Clarity prevents chaos. A culture low in decision discipline becomes paralyzed by ambiguity during a pivot, leading to wasted resources and 're-work' costs.")
    if 'piv_app' not in st.session_state:
        val = st.session_state.investments["Clarity & Decision Discipline"]
        if val < 20: st.session_state.total_budget -= 10; st.session_state.piv_res = ("FAIL: Clarity too low. -$10", "error")
        else: st.session_state.total_budget += 10; st.session_state.piv_res = ("SUCCESS: Clarity payed off! +$10", "success")
        st.session_state.piv_app = True; st.rerun()
    msg, lvl = st.session_state.piv_res
    if lvl == "success": st.success(msg)
    else: st.error(msg)

# PHASE 4: LEADERSHIP
elif current_phase == "Leadership Change":
    st.info("**STAGE: Leadership Transition**\n\n**Success Criteria:** Psychological Safety >= $20. \n**Failure Criteria:** Psychological Safety < $20.\n\n**Why it matters:** New leaders rely on the team to flag risks early. In low-safety cultures, teams hide bad news from new bosses to protect themselves, leading to catastrophic 'blind-spot' failures.")
    if 'ldr_app' not in st.session_state:
        val = st.session_state.investments["Psychological Safety"]
        if val < 20: st.session_state.total_budget -= val; st.session_state.investments["Psychological Safety"] = 0; st.session_state.ldr_res = (f"FAIL: Safety lost (${val})", "error")
        else: st.session_state.ldr_res = ("SUCCESS: Safety held.", "success")
        st.session_state.ldr_app = True; st.rerun()
    msg, lvl = st.session_state.ldr_res
    if lvl == "success": st.success(msg)
    else: st.error(msg)

# PHASE 5: HEDIS
elif current_phase == "Open Enrollment & HEDIS":
    st.info("**STAGE: OE & HEDIS Season**\n\n**Success Criteria:** Sustainable Pace > $19. \n**Failure Criteria:** Sustainable Pace <= $19.\n\n**Why it matters:** Peak seasons require 'reserve' energy. A culture that is already red-lining on pace will experience burnout-induced errors and turnover when the workload spikes.")
    if 'hed_app' not in st.session_state:
        val = st.session_state.investments["Sustainable Pace & Focus"]
        if val > 19: st.session_state.total_budget += 10; st.session_state.hed_res = ("SUCCESS: Pace held. +$10", "success")
        else: st.session_state.total_budget -= 10; st.session_state.hed_res = ("FAIL: Burnout. -$10", "error")
        st.session_state.hed_app = True; st.rerun()
    msg, lvl = st.session_state.hed_res
    if lvl == "success": st.success(msg)
    else: st.error(msg)

# PHASE 6: BUILDATHON
elif current_phase == "IT Build-a-Thon":
    st.info("**STAGE: IT Build-a-Thon**\n\n**Success Criteria:** Partnership >= $17. \n**Failure Criteria:** Partnership < $17.\n\n**Why it matters:** Innovation is a team sport. Cultures stuck in silos can't collaborate fast enough to enter—let alone win—cross-functional innovation events.")
    if 'bld_app' not in st.session_state:
        val = st.session_state.investments["Cross-Team Partnership"]
        if val < 17: st.session_state.bld_res = ("NO ENTRY.", "warning")
        elif val <= 21: st.session_state.total_budget += 5; st.session_state.bld_res = ("ENTRY AWARD: +$5", "success")
        else: st.session_state.total_budget += 10; st.session_state.bld_res = ("WINNER: +$10", "success")
        st.session_state.bld_app = True; st.rerun()
    msg, lvl = st.session_state.bld_res
    if lvl == "success": st.success(msg)
    else: st.warning(msg)

# PHASE 7: ENTERPRISE
elif current_phase == "Enterprise Project Kick-off":
    st.info("**STAGE: Enterprise Project**\n\n**Success Criteria:** Partnership > $25. \n**Failure Criteria:** Partnership <= $25.\n\n**Why it matters:** Large-scale success for GEHA requires elite-level collaboration. If partnership isn't a core competency, the project will suffer from 'boundary friction' and missed enterprise synergies.")
    if 'ent_app' not in st.session_state:
        val = st.session_state.investments["Cross-Team Partnership"]
        if val > 25: st.session_state.total_budget += 20; st.session_state.ent_res = ("SUCCESS: +$20", "success")
        else:  st.session_state.total_budget -= 20; st.session_state.ent_res = ("PROJECT FAILURE.", "warning")
        st.session_state.ent_app = True; st.rerun()
    msg, lvl = st.session_state.ent_res
    if lvl == "success": st.success(msg)
    else: st.warning(msg)

# PHASE 8: FINAL
elif current_phase == "Final Analysis":
    st.header("📊 Final Market Analysis")
    if len(st.session_state.history) < 7:
        final = st.session_state.investments.copy()
        final['Label'] = "Final Outcome"
        st.session_state.history.append(final)
    
    df = pd.DataFrame(st.session_state.history).melt(id_vars=['Label'], var_name='Behavior', value_name='Investment')
    st.plotly_chart(px.bar(df, x='Behavior', y='Investment', color='Label', barmode='group', height=600), use_container_width=True)
    
    st.divider()
    if st.button("🤖 Analyze Cultural DNA"):
        s, c, p = st.session_state.investments["Psychological Safety"], st.session_state.investments["Clarity & Decision Discipline"], st.session_state.investments["Sustainable Pace & Focus"]
        if s < 10 and c > 30: st.session_state.ai_summary = "High-precision but high-fear culture. Technical clarity hides silent human risks."
        elif p < 15: st.session_state.ai_summary = "Collaborative success built on a foundation of imminent burnout."
        else: st.session_state.ai_summary = "A resilient, high-trust model balanced for long-term GEHA success."
    
    if st.session_state.ai_summary: st.info(f"**AI Summary:** {st.session_state.ai_summary}")
    
    csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Results", data=csv, file_name=f"geha_results_{st.session_state.facilitator_name}.csv")

# LIVE FEEDBACK
if current_phase != "Final Analysis":
    st.divider()
    live_df = pd.DataFrame(list(st.session_state.investments.items()), columns=['Stock', 'Value'])
    st.plotly_chart(px.bar(live_df, x='Stock', y='Value', range_y=[0, 100], text_auto=True), use_container_width=True)
