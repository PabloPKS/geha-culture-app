import streamlit as st
import pandas as pd
from io import BytesIO

# --- APP CONFIG ---
st.set_page_config(page_title="GEHA Triage Trainer", page_icon="🚦", layout="wide")

# --- PERSISTENT DEFINITIONS (SIDEBAR) ---
with st.sidebar:
    st.header("📖 Triage Definitions")
    st.markdown("""
    ### 📡 **SIGNAL**
    **Action Now.** Affects trust, external commitments, regulatory risk, or core operations. Calm but deliberate action is justified.
    
    ---
    ### ❓ **UNKNOWN**
    **Validate First.** Feels urgent but requires context. Acting too fast increases noise or rework.
    
    ---
    ### 🌪️ **NOISE**
    **Ignore/Shield.** Distracting or emotionally charged. Pulls focus away from clarity and increases anxiety.
    """)
    st.divider()
    if 'score' in st.session_state:
        st.metric("Current Score", f"{st.session_state.score}")

# --- SCENARIOS DATA ---
scenarios = [
    {"text": "A Teams chat in the 'Fun-Stuff' channel has reached 50+ notifications because people are debating if a hotdog is a sandwich.", "category": "NOISE", "reason": "High engagement, zero impact on core operations or regulatory risk."},
    {"text": "A lead developer mentions that a recent Microsoft Graph API update 'might' break the portal connection, but logs haven't been checked.", "category": "UNKNOWN", "reason": "Potential risk, but requires a log check before escalating to a Signal."},
    {"text": "Automated high-priority alert: The SQL database for claims processing has hit 98% storage capacity.", "category": "SIGNAL", "reason": "Core operations risk. If the DB hits 100%, claims stop moving."},
    {"text": "A vendor who lost a contract bid six months ago sends a long 'read-receipt' email to the executive team complaining about the process.", "category": "NOISE", "reason": "Emotionally charged but carries no actual weight or future risk."},
    {"text": "A news headline breaks stating that a major national healthcare competitor is undergoing a surprise federal audit for HIPAA compliance.", "category": "UNKNOWN", "reason": "Industry-relevant, but context is needed to see if GEHA shares the same vulnerability."},
    {"text": "A Power BI dashboard used for executive reporting shows a 'Data Source Error' 15 minutes before the Board meeting.", "category": "SIGNAL", "reason": "Affects trust and external commitments (The Board)."},
    {"text": "A stakeholder requests a 10-year projection for a pilot program that has only been live in the 'Sandwich' environment for three weeks.", "category": "NOISE", "reason": "Premature. 10-year projections on 3 weeks of data is just 'Noise with Math.'"},
    {"text": "The 'Expected Completion Date' column in a shared SharePoint list has disappeared, and the PM isn't sure who edited the view.", "category": "UNKNOWN", "reason": "Could be a simple UI glitch (Noise) or a data loss issue (Signal). Needs validation."},
    {"text": "A senior analyst on your team suddenly clears their desk and leaves the office mid-day without telling anyone before a milestone.", "category": "SIGNAL", "reason": "Significant risk to core operations and personnel management."},
    {"text": "An anonymous tip in the suggestion box states 'leadership doesn't listen,' but no specific department is provided.", "category": "NOISE", "reason": "Too vague to be actionable; creates anxiety without a path to resolution."},
    {"text": "Microsoft announces an 'End of Life' date for an Azure framework that powers 40% of GEHA’s internal data pipelines.", "category": "SIGNAL", "reason": "Affects core operations and requires intentional coordination to migrate."},
    {"text": "A cold LinkedIn message from a startup claims their AI can reduce GEHA's overhead by 50% but includes no technical docs.", "category": "NOISE", "reason": "Standard marketing noise with no substance."},
    {"text": "A $2.5M discrepancy is found between the projected claims payout in the Python model and the actual bank wire transfer.", "category": "SIGNAL", "reason": "Affects regulatory risk, financial integrity, and core trust."},
    {"text": "A rumor in the breakroom suggests building Wi-Fi is being throttled, causing staff to worry about Teams call quality.", "category": "UNKNOWN", "reason": "Needs a quick 'Yes/No' from IT to prevent a wave of panic messages."},
    {"text": "A department head marks a Teams message as 'Urgent' to discuss the specific shade of blue used in the new internal newsletter.", "category": "NOISE", "reason": "Misuse of the 'Urgent' tag; pulls focus away from strategic priorities."}
]

# --- SESSION STATE ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.complete = False
    st.session_state.results_log = []

# --- MAIN UI ---
st.title("🚦 GEHA Information Triage Trainer")

if not st.session_state.complete:
    progress = st.session_state.index / len(scenarios)
    st.progress(progress)
    st.write(f"**Scenario {st.session_state.index + 1} of {len(scenarios)}**")

    current_item = scenarios[st.session_state.index]
    
    with st.container(border=True):
        st.subheader("Situation:")
        st.info(current_item["text"])
    
    if not st.session_state.answered:
        col1, col2, col3 = st.columns(3)
        user_choice = None
        with col1:
            if st.button("📡 SIGNAL", use_container_width=True): user_choice = "SIGNAL"
        with col2:
            if st.button("❓ UNKNOWN", use_container_width=True): user_choice = "UNKNOWN"
        with col3:
            if st.button("🌪️ NOISE", use_container_width=True): user_choice = "NOISE"
        
        if user_choice:
            st.session_state.answered = True
            st.session_state.current_choice = user_choice
            st.session_state.results_log.append({
                "Scenario": current_item["text"],
                "Your Answer": user_choice,
                "Correct Answer": current_item["category"],
                "Rationale": current_item["reason"],
                "Result": "✅ Correct" if user_choice == current_item["category"] else "❌ Incorrect"
            })
            if user_choice == current_item["category"]:
                st.session_state.score += 1
            st.rerun()

    if st.session_state.answered:
        choice = st.session_state.current_choice
        if choice == current_item["category"]:
            st.success(f"✅ **Correct!** It's a {current_item['category']}.")
        else:
            st.error(f"❌ **Incorrect.** This was a {current_item['category']}.")
        
        st.write(f"**Rationale:** {current_item['reason']}")
        
        if st.button("Next Scenario ➡️", use_container_width=True):
            if st.session_state.index < len(scenarios) - 1:
                st.session_state.index += 1
                st.session_state.answered = False
                st.rerun()
            else:
                st.session_state.complete = True
                st.rerun()

else:
    st.balloons()
    st.header("Training Complete!")
    final_pct = (st.session_state.score / len(scenarios)) * 100
    st.metric("Final Score", f"{st.session_state.score}/{len(scenarios)}", f"{final_pct:.0f}%")

    # Excel Export
    df = pd.DataFrame(st.session_state.results_log)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='TriageResults')
    processed_data = output.getvalue()

    st.download_button(
        label="📥 Download Results as Excel",
        data=processed_data,
        file_name="GEHA_Triage_Results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    if st.button("Restart Exercise"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
