# Feature: Automated Pattern Detection Briefing

Weekly "here's what's actually going on with you" — no prompt required.

## Why

A gentle summary gets ignored. The output needs to land as a direct provocation:

> *"You've mentioned feeling blocked on the same project 4 times this month but reframed it differently each time. You haven't resolved it."*

## What it detects

- **Recurring themes** — what keeps coming back unresolved
- **Energy patterns** — high vs crashing cycles
- **Stated intentions vs follow-through** — did they do the thing they said last week
- **Contradictions** — places they said opposite things across entries

## Implementation

Extend `/api/v1/llm/summarise` with a tuned system prompt:

```python
system_prompt = """You are analyzing journal entries for a person.
Focus on: recurring unresolved themes, energy/momentum patterns,
stated intentions that were or weren't followed through, and contradictions
across entries. Be direct and specific. No soft language."""
```

Schedule via cron — result ready before they wake up, zero perceived latency:

```bash
0 2 * * 0 python3 app/scripts/weekly_briefing.py
```

## v2

Ingest the art journal pages — correlate image density and color with text sentiment. Visual/emotional signal when words aren't enough.