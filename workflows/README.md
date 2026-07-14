# n8n Workflows

This directory contains the exported JSON workflows for the 3-agent AI Job Intelligence pipeline.

## Files

1. **`01-scraper-agent.json`**: (Agent 1) Scrapes job boards (Internshala, RemoteOK, HackerNews) at 7 AM daily, deduplicates against existing jobs, scores them using Groq (`openai/gpt-oss-120b`), and commits the updated dataset back to GitHub.
2. **`02-scoring-agent.json`**: (Agent 2) Runs at 8 AM daily, pulls the top 5 highest-scoring jobs from GitHub, extracts ATS keywords via Groq, generates a tailored Harvard-style resume, computes an ATS match score, and commits both the resume and ATS report back to GitHub.
3. **`03-digest-agent.json`**: (Agent 3) Sends a formatted email digest of the top 5 jobs. Includes an "APPROVE" button powered by an n8n webhook. When clicked, it fetches the tailored resume and ATS report from GitHub and emails them back to the candidate.

## How to Import

1. Open your n8n workspace.
2. Click **Add workflow** in the top right corner.
3. From the top-right menu (`...`), select **Import from file...**.
4. Select one of the `.json` files in this directory.
5. You will need to recreate your credentials (e.g., GitHub Personal Access Token, Groq API Key, Gmail SMTP) when prompted, as they have been strictly redacted for security.
6. Make sure to activate the workflows by toggling the switch in the top right!
