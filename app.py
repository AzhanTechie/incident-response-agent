import os
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

BANK_ID = "incident-agent"

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY"),
)
groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Incident Response Agent", layout="centered")
st.title("Incident Response Agent")
st.caption("Powered by Hindsight memory — recalls similar past incidents and learns from every new one.")

incident_text = st.text_area(
    "Describe the new incident",
    height=100,
    placeholder="e.g. Payment service returning 500 errors during checkout, connection timeouts...",
)

if st.button("Analyze incident", type="primary"):
    if not incident_text.strip():
        st.warning("Please describe the incident first.")
    else:
        with st.spinner("Recalling similar past incidents from memory..."):
            recalled = hindsight.recall(
                bank_id=BANK_ID,
                query=incident_text,
                types=["world", "experience", "observation"],
                max_tokens=2000,
            )

        st.subheader("Recalled from memory")
        if recalled.results:
            for r in recalled.results[:8]:
                st.markdown(f"- {r.text}")
        else:
            st.info("No related past incidents found yet — this looks like a new type of issue.")

        with st.spinner("Analyzing..."):
            system_prompt = (
                "You are an incident response assistant. You are given a new incident "
                "and related past incidents from memory, including root causes and "
                "resolutions. Suggest a likely root cause and a recommended action. "
                "If a past incident is clearly similar, reference it. Be concise: 3-5 sentences."
            )
            memory_context = (
                "\n".join(f"- {r.text}" for r in recalled.results)
                if recalled.results
                else "No related past incidents found."
            )
            response = groq.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"New incident:\n{incident_text}\n\nRelated past incidents:\n{memory_context}"},
                ],
            )
            analysis = response.choices[0].message.content

        st.subheader("Agent analysis")
        st.success(analysis)

        st.session_state["last_incident"] = incident_text

with st.expander("Teach the agent what actually happened (optional)"):
    resolution = st.text_area("Actual resolution", height=80, key="resolution_input")
    if st.button("Save resolution to memory"):
        if "last_incident" not in st.session_state:
            st.warning("Analyze an incident first.")
        elif not resolution.strip():
            st.warning("Describe the resolution first.")
        else:
            import uuid
            hindsight.retain(
                bank_id=BANK_ID,
                content=f"Incident: {st.session_state['last_incident']}\nActual resolution: {resolution}",
                context="incident postmortem",
                document_id=f"inc-{uuid.uuid4().hex[:8]}",
                tags=["incident"],
            )
            st.success("Saved. Future incidents will benefit from this.") 