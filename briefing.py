import feedparser
import re
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from groq import Groq

# --- Setup ---
client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

sources = [
    "https://techcrunch.com/feed/",
    "https://www.technologyreview.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://arxiv.org/rss/cs.AI"
]

keywords = [
    "AI", "artificial intelligence", "robotics",
    "LLM", "machine learning", "automation",
    "GPT", "neural network", "deep learning",
    "large language model", "generative AI"
]

# --- Filter Function ---
def is_relevant(text, keywords):
    for keyword in keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

# --- Fetch and Filter Articles ---
filtered_articles = []

for url in sources:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title
        summary = entry.summary if hasattr(entry, 'summary') else ""
        if is_relevant(title, keywords) or is_relevant(summary, keywords):
            filtered_articles.append({
                "title": entry.title,
                "link": entry.link,
                "source": feed.feed.title,
                "summary": summary
            })

print(f"Found {len(filtered_articles)} relevant articles. Summarizing top 15...")

# --- Summarize with Groq ---
articles_text = ""
for i, article in enumerate(filtered_articles[:15]):
    articles_text += f"{i+1}. {article['title']}\nSummary: {article['summary'][:300]}\nLink: {article['link']}\n\n"

prompt = f"""
You are a tech news analyst writing a daily briefing email for a professional audience.
Below are today's relevant AI and robotics news headlines and summaries.

{articles_text}

Please provide a structured briefing in exactly this format for each article:

1. [Exact Article Headline]
[2-3 sentence summary of this specific article only, no general commentary]
Link: [article link]

2. [Exact Article Headline]
[2-3 sentence summary of this specific article only, no general commentary]
Link: [article link]

Continue this format for all articles.

Rules:
- Do NOT include any overall summary or introduction
- Do NOT include Trend to Watch or Bottom Line sections
- Do NOT use phrases like "Why it matters"
- Each article gets its own specific summary only
- Keep each summary factual and to the point
"""

response = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    model="llama-3.3-70b-versatile",
)

briefing_text = response.choices[0].message.content
print("Briefing generated. Sending email...")

# --- Email Function ---
def send_briefing_email(briefing_text):
    sender = os.environ.get('GMAIL_ADDRESS')
    password = os.environ.get('GMAIL_APP_PASSWORD')
    receiver = os.environ.get('GMAIL_ADDRESS')
    receiver2 = os.environ.get('GMAIL_RECEIVER2')
    receiver3 = os.environ.get('GMAIL_RECEIVER3')

    all_receivers = [r for r in [receiver, receiver2, receiver3] if r]

    # --- Parse articles into sections ---
    sections = ""
    blocks = briefing_text.strip().split("\n\n")

    for block in blocks:
        if not block.strip():
            continue

        lines = block.strip().split("\n")
        headline = ""
        summary_lines = []
        link = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line[0].isdigit() and ". " in line:
                headline = line.split(". ", 1)[1] if ". " in line else line
            elif line.lower().startswith("link:"):
                link = line.replace("Link:", "").replace("link:", "").strip()
            else:
                summary_lines.append(line)

        summary = " ".join(summary_lines)

        if headline:
            link_html = f'<a href="{link}" style="color: #1D6FA4; font-size: 13px; font-weight: 500; text-decoration: underline;">Read full article →</a>' if link else ""
            sections += f"""
            <div style="background-color: #ffffff; padding: 25px 30px; border-radius: 0px; margin-top: 15px; border-left: 4px solid #1D6FA4; border-bottom: 1px solid #eeeeee;">
                <h2 style="font-family: 'Bebas Neue', Georgia, serif; color: #000000; font-size: 22px; font-weight: bold; margin: 0 0 10px 0; letter-spacing: 1px;">{headline}</h2>
                <p style="font-family: 'Inter', Arial, sans-serif; color: #333333; font-size: 15px; line-height: 1.8; margin: 0 0 12px 0;">{summary}</p>
                {link_html}
            </div>
            """

    # --- Build HTML email ---
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Raleway:wght@300&family=Bebas+Neue&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    </head>
    <body style="font-family: 'Inter', Arial, sans-serif; max-width: 700px; margin: auto; padding: 20px; background-color: #ffffff;">

        <div style="padding: 30px; text-align: center;">
            <h1 style="font-family: 'Playfair Display', Georgia, serif; color: #000000; font-size: 56px; margin: 0; letter-spacing: 2px; font-weight: 700;">AI & Robotics</h1>
            <p style="font-family: 'Raleway', sans-serif; color: #555555; margin: 8px 0 0 0; font-size: 14px; letter-spacing: 4px; text-transform: uppercase; font-weight: 300;">Daily Briefing</p>
        </div>

        {sections}

        <div style="text-align: center; margin-top: 20px; padding: 15px;">
            <p style="color: #aaaaaa; font-size: 12px; letter-spacing: 1px;">Generated Automatically by a Custom Built Tech News Tool</p>
        </div>

    </body>
    </html>
    """

    # --- Set up and send email ---
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "💡 Your Daily AI & Robotics Briefing 🤖"
    msg["From"] = sender
    msg["To"] = ", ".join(all_receivers)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, all_receivers, msg.as_string())
        print("✅ Briefing email sent successfully!")

send_briefing_email(briefing_text)
