# Incident Response Agent

An AI agent that helps engineers diagnose production incidents by recalling similar past incidents from persistent memory — built with [Hindsight](https://hindsight.vectorize.io/) by Vectorize.

## Problem

Engineers waste time re-diagnosing incidents that look like past ones, because there's no memory layer connecting "this happened before" to "here's what fixed it." Every incident starts from zero.

## How it works

1. A new incident is described in plain text.
2. The agent **recalls** semantically similar past incidents from a Hindsight memory bank — root causes, symptoms, and resolutions — even when the wording doesn't match.
3. An LLM (via Groq, `openai/gpt-oss-120b`) reasons over the recalled memories and suggests a likely root cause and next action.
4. Once the real resolution is known, it's **retained** back into memory — so the very next similar incident benefits from what was just learned.

This demonstrates the full retain → recall loop: the agent visibly gets smarter with each new incident, rather than starting from zero every time.

## Tech stack

- **Memory**: Hindsight Cloud
- **LLM**: Groq (`openai/gpt-oss-120b`)
- **UI**: Streamlit
- **Language**: Python

## Setup

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

Create a .env file with: HINDSIGHT_API_KEY=your_hindsight_key
GROQ_API_KEY=your_groq_key


Seed the memory bank with example past incidents:
```bash
python seed_incidents.py
```

Run the app:
```bash
streamlit run app.py
```

## Demo video

[ https://youtu.be/9tuUN9BmQOs?si=UenTueb4yDfq-vCf ]

## Team

[ - Mohammed Azhan Tehami
- Mohd Syfiyaan Ali
- Mohd Nayab Aman Hussain
- Mohammed Najeebuddin
- Omar Khan
- Mohammed Huzaifa Hussaini ]