import streamlit as st
import random

# --- APP CONFIG ---
st.set_page_config(page_title="GEHA Information Triage Trainer", page_icon="🚦")

# --- SCENARIOS DATA ---
scenarios = [
    {"text": "A Teams chat in the 'Fun-Stuff' channel has reached 50+ notifications debating if a hotdog is a sandwich.", "category": "NOISE", "reason": "High engagement, zero impact on core operations or regulatory risk."},
    {"text": "A lead developer mentions that a recent Microsoft Graph API update 'might' break the portal connection, but logs haven't been checked.", "category": "UNKNOWN", "reason": "Potential risk, but requires a log check before escalating to a Signal."},
    {"text": "Automated high-priority alert: The SQL database for claims processing has hit 98% storage capacity.", "category": "SIGNAL", "reason": "Core operations risk. If the DB hits 100%, claims stop moving."},
    {"text": "A vendor who lost a contract bid six months ago sends a long 'read-receipt' email to the executive team complaining about the process.", "category": "NOISE", "reason": "Emotionally charged but carries no actual weight or future risk."},
    {"text": "A Power BI dashboard used for executive reporting shows a 'Data Source Error' 15 minutes before the Board meeting.", "category": "SIGNAL", "reason": "Affects trust and external commitments (The Board)."},
    {"text": "A stakeholder requests a 10-year projection for a pilot program that has only been live in the 'Sandwich' environment for three weeks.", "category": "NOISE", "reason": "Premature. 10-year projections on 3 weeks of data is just 'Noise with Math.'"},
    {"text": "A senior analyst on your team suddenly clears their desk and leaves the office mid-day without telling anyone before a milestone.", "category": "SIGNAL", "reason": "Significant risk to core operations and personnel management."},
    {"text": "A $2.5M discrepancy is found between the projected claims payout in the Python model and the actual bank wire transfer.", "category": "SIGNAL", "reason": "Affects regulatory risk, financial integrity, and core trust."},
    {"text": "A department head marks a Teams message as 'Urgent' to discuss the specific shade of blue used in the new newsletter.", "category": "NOISE", "reason": "Misuse of the 'Urgent' tag; pulls focus away from strategic priorities."},
    {"text": "A rumor in the breakroom suggests building Wi-Fi is being throttled, causing staff to worry about Teams call quality.", "category": "UNKNOWN", "reason": "Needs a quick 'Yes/No' from IT to prevent a wave of panic messages."}
]

# --- SESSION STATE INITIALIZATION ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.complete = False

# --- UI ---
st.title("🚦 GEHA Information Triage Trainer")
st.markdown("""
Use this tool to practice categorizing information. Remember:
* **SIGNAL**: Requires action now. Affects trust, risk, or operations.
* **UNKNOWN**: Requires validation or context before acting.
* **NOISE**: Distracting/Emotionally charged. Does not need action.
""")

if not st.session_state.complete:
    current_item = scenarios[st.session_state.index]
    
    st.subheader(f"Scenario {st.session_state.index + 1} of {len(scenarios)}")
    st.info(current_item["text"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📡 SIGNAL"):
            user_choice = "SIGNAL"
    with col2:
        if st.button("❓ UNKNOWN"):
            user_choice = "UNKNOWN"
    with col3:
        if st.button("🌪️ NOISE"):
            user_choice = "NOISE"
            
    # Logic to handle the choice
    if 'user_choice' in locals():
        if user_choice == current_item["category"]:
            st.success(f"**Correct!** {current_item['reason']}")
            st.session_state.score += 1
        else:
            st.error(f"**Incorrect.** This was actually a **{current_item['category']}**. {current_item['reason']}")
        
        if st.button("Next Scenario ➡️"):
            if st.session_state.index < len(scenarios) - 1:
                st.session_state.index += 1
                st.rerun()
            else:
                st.session_state.complete = True
                st.rerun()

else:
    st.balloons()
    st.header("Training Complete!")
    final_score = (st.session_state.score / len(scenarios)) * 100
    st.metric("Final Score", f"{final_score:.0f}%")
    
    if st.button("Restart Training"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.complete = False
        st.rerun()
