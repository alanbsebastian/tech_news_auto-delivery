# Daily Tech News Briefing

An automated daily news briefing tool that monitors the web for the latest developments in tech, summarizes them using a large language model, and delivers a clean formatted email every morning.

---

## What It Does

- Pulls articles from multiple major tech and AI news sources every day
- Filters only relevant content using keyword matching with regex
- Summarizes each article using the LLaMA 3.3 70B model via Groq API
- Delivers a professionally formatted HTML email briefing automatically every morning

---

## How It Works

```
RSS Feeds → Filter by Keywords → Summarize with LLaMA (Groq) → Send via Gmail SMTP
```

1. **Fetch** — Pulls live RSS feeds from TechCrunch, MIT Technology Review, The Verge, Wired, and ArXiv
2. **Filter** — Scans titles and summaries for tech keywords using regex word boundary matching
3. **Summarize** — Sends filtered articles to Groq's LLaMA 3.3 70B model with a structured prompt
4. **Deliver** — Sends a clean HTML formatted email to configured recipients via Gmail SMTP

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| News Fetching | feedparser, RSS |
| AI Summarization | Groq API, LLaMA 3.3 70B |
| Email Delivery | Gmail SMTP, Python smtplib |
| Automation | GitHub Actions, cron scheduling |
| Secret Management | GitHub Secrets, environment variables |

---

## News Sources

- [TechCrunch](https://techcrunch.com)
- [MIT Technology Review](https://www.technologyreview.com)
- [The Verge](https://www.theverge.com)
- [Wired](https://www.wired.com)
- [ArXiv — AI Research Papers](https://arxiv.org/list/cs.AI/recent)

---

## Want to Build Your Own?

Fork this repository and add your own API keys and Gmail credentials as GitHub Secrets. See the Setup section below.

---

## Setup

### 1. Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |
| `GMAIL_ADDRESS` | Your Gmail address |
| `GMAIL_APP_PASSWORD` | Your Gmail App Password |
| `GMAIL_RECEIVER2` | Second recipient email (optional) |
| `GMAIL_RECEIVER3` | Third recipient email (optional) |

### 2. Schedule

The workflow runs automatically via GitHub Actions every day. Timing is set in `.github/workflows/daily_briefing.yml` using cron syntax.

---

## Project Structure

```
tech_news_auto-delivery/
├── briefing.py
└── .github/
    └── workflows/
        └── daily_briefing.yml
```

---

## Key Concepts Used

- **RSS parsing** — fetching and parsing live XML data feeds
- **Regex filtering** — word boundary matching to avoid false positives
- **Prompt engineering** — structured prompts for consistent LLM output
- **SMTP protocol** — programmatic email delivery
- **CI/CD scheduling** — automated execution via GitHub Actions cron
- **Environment variables** — secure secret management in production

---

*Generated Automatically by a Custom Built Tech News Tool*
