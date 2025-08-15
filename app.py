import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name = "Qwen/Qwen3-8B-FP8" 
tokenizer = AutoTokenizer.from_pretrained(model_name)
qwen_pipeline = pipeline(
    "text-generation",
    model=AutoModelForCausalLM.from_pretrained(model_name, device_map="auto"),
    tokenizer=tokenizer
)

class QwenWrapper:
    def generate_content(self, prompt):
        output = qwen_pipeline(prompt) 
        class Resp:
            text = output[0]["generated_text"].strip()
        return Resp()

model = QwenWrapper()

def search_news(company):
    """Scrape Bing News for the latest company news (robust version)."""
    query = quote(f"{company} latest news")
    url = f"https://www.bing.com/news/search?q={query}&qft=sortbydate='1'"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    company_keywords = [word.lower() for word in company.split()]
    articles = []

    headline_selectors = [
        "div.news-card a",
        "div.news-card-body a",
        "a.title",
        "a.t_t",
        "h2 a"
    ]
    seen_links = set()

    for selector in headline_selectors:
        for a_tag in soup.select(selector):
            link = a_tag.get("href")
            title = a_tag.get_text(strip=True)
            if not link or not title:
                continue
            if link in seen_links:
                continue
            if not any(kw in title.lower() for kw in company_keywords):
                continue
            seen_links.add(link)
            articles.append((title, link))

    return articles[:5]

def fetch_article_text(url):
    """Fetch full article text."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return " ".join(p.get_text() for p in soup.find_all("p"))
    except:
        return ""

def summarize_with_qwen(article_text, company, style="neutral"):
    """Summarize article text with Qwen in a given style."""
    style_prompts = {
        "Formal business summary": "Provide a professional business-style summary.",
        "Casual conversation": "Summarize it in a friendly, casual tone.",
        "Quick bullet points": "Summarize it in 3-5 concise bullet points.",
        "neutral": "Provide a clear, factual summary."
    }
    style_instruction = style_prompts.get(style, style_prompts["neutral"])
    prompt = f"{style_instruction} The article is about {company}.\n\n{article_text}"
    try:
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except:
        return "Unable to summarize this article."

def extract_company_from_query(query):
    """Use Qwen to extract the company name from a user query."""
    prompt = f"Extract only the main company name from this query, no extra words: '{query}'"
    try:
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except:
        return None

def handle_user_message(user_msg):
    """Handle chatbot requests, including fetching news if needed."""
    lower_msg = user_msg.lower()
    if "news" in lower_msg or "latest" in lower_msg:
        possible_company = extract_company_from_query(user_msg)
        if possible_company:
            articles = search_news(possible_company)
            if not articles:
                return f"Sorry, I couldn't find recent news for {possible_company}."
            summaries = []
            for title, link in articles:
                article_text = fetch_article_text(link)
                if len(article_text) < 100:
                    continue
                summary = summarize_with_qwen(article_text, possible_company)
                summaries.append(f"**{title}**\n{summary}\n[Read more]({link})")
            if summaries:
                return "\n\n".join(summaries)
            else:
                return f"Found news articles for {possible_company}, but couldn't summarize them."
        else:
            return "Please specify the company you want news about."

    conversation_text = "\n".join(
        f"{'User' if m['role']=='user' else 'Qwen'}: {m['content']}"
        for m in st.session_state.messages
    )
    try:
        resp = model.generate_content(conversation_text)
        return resp.text.strip()
    except:
        return "Sorry, I couldn't process that."

st.set_page_config(page_title="Company News Chatbot", page_icon="📈", layout="wide")
st.title("📈 Company News Chatbot (Live Search)")

mode = st.radio("Choose Mode", ["Company News", "Chatbot"])

if mode == "Company News":
    companies_input = st.text_input("Enter company names (comma separated)")
    style = st.selectbox(
        "Choose style",
        [
            "Formal business summary",
            "Casual conversation",
            "Quick bullet points"
        ]
    )
    if st.button("Get Latest News"):
        companies = [c.strip() for c in companies_input.split(",") if c.strip()]
        if not companies:
            st.warning("Please enter at least one company name.")
        else:
            for company in companies:
                st.subheader(f"📰 {company} - Latest News")
                articles = search_news(company)
                if not articles:
                    st.write("No recent news found.")
                    continue
                for title, link in articles:
                    article_text = fetch_article_text(link)
                    if len(article_text) < 100:
                        continue
                    summary = summarize_with_qwen(article_text, company, style)
                    st.markdown(f"**{title}**\n\n{summary}\n\n[Read more]({link})")

elif mode == "Chatbot":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        role = "🧑 You" if msg["role"] == "user" else "🤖"
        st.markdown(f"**{role}:** {msg['content']}")

    user_msg = st.chat_input("Type your message...")
    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        bot_reply = handle_user_message(user_msg)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()
