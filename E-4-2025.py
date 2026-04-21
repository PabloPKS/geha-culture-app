import streamlit as st
import pandas as pd
from io import BytesIO
import random

# --- APP CONFIG ---
st.set_page_config(page_title="GEHA Triage Trainer", page_icon="🚦", layout="wide")

# --- SCENARIOS DATA ---
raw_scenarios = [
    {
        "text": "A business user marks a data request as 'Critical Emergency' and pings the whole team. You discover they sat on the requirement for 2 weeks and now need it by EOD to meet their own deadline.", 
        "category": "NOISE", 
        "reason": "Because no regulatory risk or core operational failure was explicitly stated, this remains NOISE. Procrastination does not automatically create a Signal."
    },
    {"text": "Scott sends a direct message: 'The Board has shifted priority to the PBM integration. Put all other data migrations on hold immediately.'", "category": "SIGNAL", "reason": "Explicitly involves a Board commitment and core operational pivot."},
    {"text": "Srini asks on a leadership call: 'I've been seeing buzz about automated claims models at other carriers. Does anyone know if that fits our tech stack or if we have a gap?'", "category": "UNKNOWN", "reason": "Requires validation to determine future impact; not yet an explicit commitment or risk."},
    {"text": "Pablo asks in a meeting: 'Hey, has anyone looked into those new data privacy regulations in California? I wonder if they affect our 2027 roadmap.'", "category": "UNKNOWN", "reason": "Direct reference to regulatory investigation; requires validation before action."},
    {"text": "Hiro sends an 'Urgent' Teams invite to debate whether the 'Submit' button on the internal site should be rounded or square.", "category": "NOISE", "reason": "No explicit trust, regulatory, or core operational risk mentioned."},
    {"text": "A Teams chat in the 'Fun-Stuff' channel has reached 50+ notifications because people are debating if a hotdog is a sandwich.", "category": "NOISE", "reason": "Standard operational distraction with no business impact."},
    {"text": "A lead developer mentions that a recent Microsoft Graph API update 'might' break the portal connection, but logs haven't been checked.", "category": "UNKNOWN", "reason": "Potential core operation failure mentioned; requires validation to confirm."},
    {"text": "Automated high-priority alert: The SQL database for claims processing has hit 98% storage capacity.", "category": "SIGNAL", "reason": "Explicit core operations risk; inaction will stop claims processing."},
    {"text": "A vendor who lost a contract bid six months ago sends a long 'read-receipt' email complaining about the process.", "category": "NOISE", "reason": "Emotionally charged but no explicit regulatory or operational risk."},
    {"text": "A news headline breaks stating that major competitors have had started to have surprise federal audit from OPM to reivew HIPAA compliance.", "category": "UNKNOWN", "reason": "Potential regulatory implication; needs validation to check GEHA's exposure."},
    {"text": "A Power BI dashboard used for executive reporting shows a 'Data Source Error' 15 minutes before the Board meeting.", "category": "SIGNAL", "reason": "Explicitly affects executive trust and a high-stakes commitment."},
    {"text": "A stakeholder requests a 10-year projection for a pilot program that has only been live in the 'Sandwich' environment for three weeks.", "category": "NOISE", "reason": "No explicit risk or core operation mentioned; premature and distracting."},
    {"text": "The 'Expected Completion Date' column in a shared SharePoint list has disappeared, and the PM isn't sure who edited the view.", "category": "UNKNOWN", "reason": "Potential impact on commitments; needs validation to assess depth of data loss."},
    {"text": "A senior analyst on your team suddenly clears their desk and leaves the office mid-day without telling anyone before a milestone.", "category": "SIGNAL", "reason": "Explicit risk to core operations and resource commitments."},
    {"text": "An anonymous tip in the suggestion box states 'leadership is clueless,' but no specific department or leader is provided.", "category": "NOISE", "reason": "Vague; no specific operation or trust breach explicitly articulated."},
    {"text": "Microsoft announces an 'End of Life' date for an Azure framework that powers 40% of GEHA’s internal data pipelines.", "category": "SIGNAL", "reason": "Explicit future failure of core operations."},
    {"text": "A cold LinkedIn message from a startup claims their AI can reduce GEHA's overhead by 50% but includes no technical docs.", "category": "NOISE", "reason": "Standard vendor noise; no explicit risk or operation involved."},
    {"text": "A $2.5M discrepancy is found between the projected claims payout in the Python model and the actual bank wire transfer.", "category": "SIGNAL", "reason": "Explicit regulatory and financial risk."},
    {"text": "A rumor that a senior leader is being forced out due to an ethical disagreement over member data handling.", "category": "UNKNOWN", "reason": "This impacts the 'Trust' pillar. It requires quiet validation to determine if it is a Signal (cultural shift) or Noise (gossip) before reacting."},
    {"text": "A department head marks a Teams message as 'Urgent' to discuss the specific shade of blue used in the new internal newsletter.", "category": "NOISE", "reason": "Explicitly cosmetic; no risk to core operations or trust."},
    {"text": "A news headline says a major cloud provider had a localized outage in the 'EU-West' region; GEHA's data is strictly in 'US-Central'.", "category": "NOISE", "reason": "Explicitly outside GEHA's operational zone."}
]

# --- SESSION STATE ---
if 'scenarios' not in st.session_state:
    shuffled = raw_scenarios.copy()
    random.shuffle(shuffled)
    st.session_state.scenarios = shuffled
    
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.questions_done = 0
    st.session_state.answered = False
    st.session_state.complete = False
    st.session_state.results_log = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("📖 Triage Definitions")
    st.markdown("""
    ### 📡 **SIGNAL**
    **Action Now.** Affects trust, regulatory risk, or core operations.
    
    ---
    ### ❓ **UNKNOWN**
    **Validate First.** Requires context before acting to avoid rework.
    
    ---
    ### 🌪️ **NOISE**
    **Ignore/Shield.** Distracting. Pulls focus away from clarity.
    """)
    st.divider()
    
    if st.session_state.questions_done > 0:
        accuracy = (st.session_state.score / st.session_state.questions_done) * 100
        st.metric("Current Accuracy", f"{st.session_state.score} / {st.session_state.questions_done}", f"{accuracy:.0f}%")

# --- MAIN UI ---
st.title("🚦 GEHA Information Triage Trainer")

if not st.session_state.complete:
    # UPDATED VALIDATION PRINCIPLE
    st.warning("""
    **The Validation Principle:** If something feels like **Noise** but may carry hidden risk (e.g., a Legal request that could have regulatory implications), treat it briefly as **Unknown** to validate the facts before demoting it.
    
    **Exercise Rule:** Unless **trust, regulatory risk, or core operations** are explicitly stated, classify the item as **Noise**.
    """)

    progress = st.session_state.index / len(st.session_state.scenarios)
    st.progress(progress)
    st.write(f"**Scenario {st.session_state.index + 1} of {len(st.session_state.scenarios)}** (Randomized)")

    current_item = st.session_state.scenarios[st.session_state.index]
    
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
            st.session_state.questions_done += 1
            st.session_state.current_choice = user_choice
            
            is_correct = user_choice == current_item["category"]
            if is_correct:
                st.session_state.score += 1
                
            st.session_state.results_log.append({
                "Scenario": current_item["text"],
                "Your Answer": user_choice,
                "Correct Answer": current_item["category"],
                "Rationale": current_item["reason"],
                "Result": "✅ Correct" if is_correct else "❌ Incorrect"
            })
            st.rerun()

    if st.session_state.answered:
        choice = st.session_state.current_choice
        if choice == current_item["category"]:
            st.success(f"✅ **Correct!** It's a {current_item['category']}.")
        else:
            st.error(f"❌ **Incorrect.** This was a {current_item['category']}.")
        
        st.write(f"**Rationale:** {current_item['reason']}")
        
        if st.button("Next Scenario ➡️", use_container_width=True):
            if st.session_state.index < len(st.session_state.scenarios) - 1:
                st.session_state.index += 1
                st.session_state.answered = False
                st.rerun()
            else:
                st.session_state.complete = True
                st.rerun()

else:
    st.balloons()
    st.header("Training Complete!")
    st.metric("Final Accuracy", f"{st.session_state.score} / {len(st.session_state.scenarios)}", f"{(st.session_state.score/len(st.session_state.scenarios))*100:.0f}%")

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

    if st.button("Restart & Reshuffle Scenarios"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
