import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="GEHA Triage Trainer", page_icon="🚦", layout="centered")

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
    {"text": "A department head marks a Teams message as 'Urgent' to discuss the specific shade of blue used in the new newsletter.", "category": "NOISE", "reason": "Misuse of the 'Urgent' tag; pulls focus away from strategic priorities."}
]

# --- SESSION STATE ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.last_result = None
    st.session_state.complete = False

# --- UI ---
st.title("🚦 GEHA Information Triage Trainer")
st.write("Categorize the incoming information to reduce organizational anxiety.")

if not st.session_state.complete:
    # Progress
    progress = st.session_state.index / len(scenarios)
    st.progress(progress)
    st.write(f"Question {st.session_state.index + 1} of {len(scenarios)}")

    current_item = scenarios[st.session_state.index]
    
    with st.container(border=True):
        st.subheader("Scenario:")
        st.info(current_item["text"])
    
    # Selection Buttons
    if not st.session_state.answered:
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📡 SIGNAL", use_container_width=True):
                st.session_state.user_choice = "SIGNAL"
                st.session_state.answered = True
        with col2:
            if st.button("❓ UNKNOWN", use_container_width=True):
                st.session_state.user_choice = "UNKNOWN"
                st.session_state.answered = True
        with col3:
            if st.button("🌪️ NOISE", use_container_width=True):
                st.session_state.user_choice = "NOISE"
                st.session_state.answered = True
        
        if st.session_state.answered:
            st.rerun()

    # Feedback Logic
    if st.session_state.answered:
        if st.session_state.user_choice == current_item["category"]:
            st.success(f"✅ **Correct!** It's a {current_item['category']}.")
            if st.session_state.last_result != st.session_state.index:
                st.session_state.score += 1
                st.session_state.last_result = st.session_state.index
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

    st.sidebar.metric("Current Score", f"{st.session_state.score}/{len(scenarios)}")

else:
    st.balloons()
    st.header("Training Complete!")
    final_percentage = (st.session_state.score / len(scenarios)) * 100
    st.metric("Final Accuracy", f"{final_percentage:.0f}%")
    
    if final_percentage == 100:
        st.success("Master of Clarity! You've filtered out all the noise.")
    elif final_percentage >= 70:
        st.info("Strong Triage Skills. You're keeping the team focused.")
    else:
        st.warning("Keep practicing. Don't let the Noise become a Signal!")

    if st.button("Restart Exercise"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
