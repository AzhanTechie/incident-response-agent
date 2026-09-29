import os
import sys
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


def analyze_incident(new_incident: str):
    # Step 1: Recall similar past incidents from Hindsight
    recalled = hindsight.recall(
        bank_id=BANK_ID,
        query=new_incident,
        types=["world", "experience", "observation"],
        max_tokens=2000,
    )

    if recalled.results:
        memory_context = "\n".join(f"- {r.text}" for r in recalled.results)
    else:
        memory_context = "No related past incidents found in memory."

    print("\n--- RECALLED FROM MEMORY ---")
    print(memory_context)

    # Step 2: Ask the LLM to reason using the recalled memory
    system_prompt = (
        "You are an incident response assistant. You are given a new incident "
        "and a list of related past incidents from memory, including their root "
        "causes and how they were resolved. Use the past incidents to suggest a "
        "likely root cause and a recommended action for the new incident. "
        "If a past incident is clearly similar, explicitly reference it and say "
        "so. Be concise: 3-5 sentences."
    )

    user_prompt = f"New incident:\n{new_incident}\n\nRelated past incidents from memory:\n{memory_context}"

    response = groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    print("\n--- AGENT ANALYSIS ---")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    new_incident = (
        "Incident: Payment service returning 500 errors on checkout during a promo sale. "
        "Symptoms: spike in HTTP 500s from payment-service, connection timeouts, checkout success rate dropped."
    )
    analyze_incident(new_incident) 

    import os
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


def analyze_incident(new_incident: str):
    recalled = hindsight.recall(
        bank_id=BANK_ID,
        query=new_incident,
        types=["world", "experience", "observation"],
        max_tokens=2000,
    )

    memory_context = (
        "\n".join(f"- {r.text}" for r in recalled.results)
        if recalled.results
        else "No related past incidents found in memory."
    )

    print("\n--- RECALLED FROM MEMORY ---")
    print(memory_context)

    system_prompt = (
        "You are an incident response assistant. You are given a new incident "
        "and related past incidents from memory, including root causes and "
        "resolutions. Suggest a likely root cause and a recommended action. "
        "If a past incident is clearly similar, reference it. Be concise: 3-5 sentences."
    )
    user_prompt = f"New incident:\n{new_incident}\n\nRelated past incidents from memory:\n{memory_context}"

    response = groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    analysis = response.choices[0].message.content
    print("\n--- AGENT ANALYSIS ---")
    print(analysis)
    return analysis


def retain_outcome(incident_id: str, incident: str, actual_resolution: str):
    """Store what actually happened, so future incidents benefit from it."""
    hindsight.retain(
        bank_id=BANK_ID,
        content=f"Incident: {incident}\nActual resolution: {actual_resolution}",
        context="incident postmortem",
        document_id=incident_id,
        tags=["incident"],
    )
    print(f"\n--- RETAINED {incident_id} INTO MEMORY ---")


if __name__ == "__main__":
    new_incident = (
        "Incident: Payment service returning 500 errors on checkout during a promo sale. "
        "Symptoms: spike in HTTP 500s from payment-service, connection timeouts, checkout success rate dropped."
    )

    analyze_incident(new_incident)

    # Simulate the engineer confirming what actually fixed it
    retain_outcome(
        incident_id="inc-006",
        incident=new_incident,
        actual_resolution="Increased DB_CONNECTION_POOL_SIZE to 40 ahead of the promo and "
                           "enabled autoscaling on pool usage. Resolved in 4 minutes.",
    )

    print("\n\n=== RUNNING A SIMILAR NEW INCIDENT AGAIN, NOW THAT inc-006 IS IN MEMORY ===")
    followup_incident = (
        "Incident: Payment service 500 errors and timeouts during a flash sale, "
        "connection pool related."
    )
    analyze_incident(followup_incident)