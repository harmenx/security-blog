import os
import sys
import datetime
import requests
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_security_news(api_key):
    """Fetches security news from the NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q=cybersecurity&apiKey={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["articles"]

def generate_content_from_article(article):
    """Generates a blog post from a news article."""
    title = article["title"]
    content = article["content"]
    
    if not content:
        content = "No content available for this article."

    prompt = f"""
Please write a blog post about the following article:
Title: {title}
Content: {content}

The blog post should have the following structure:
- A summary of the article.
- An analysis of the article.
- A conclusion.
"""

    client = OpenAI(
        api_key=os.getenv("POE_API_KEY"),
        base_url="https://api.poe.com/v1"
    )
    
    completion = client.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024, # Increased max_tokens for potentially longer prompts with news
    )

    response = completion.choices[0].message.content

    blog_post = f"""
## {title}

{response}
"""
    return blog_post

def create_jekyll_post(article, content):
    """Creates a Jekyll post from a news article."""
    title = article["title"]
    
    # Generate filename
    today = datetime.datetime.now()
    filename_date = today.strftime("%Y-%m-%d")
    filename_title = title.lower().replace(" ", "-").replace(":", "").replace(",", "").replace("'", "")
    filename = f"{filename_date}-{filename_title}.md"

    # Construct front matter
    front_matter = f"""
---
layout: post
title: \"{title}\" 
date: {today.strftime("%Y-%m-%d %H:%M:%S %z")}
categories: ["security", "news"]
tags: ["cybersecurity", "news", "analysis"]
seo_title: \"{title}\" 
description: \"{article['description']}\" 
---

"""
    return filename, front_matter + content

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    poe_api_key = os.getenv("POE_API_KEY")

    if not api_key:
        print("Error: API_KEY environment variable not set.")
        sys.exit(1)
        
    if not poe_api_key:
        print("Error: POE_API_KEY environment variable not set.")
        sys.exit(1)

    print("Fetching security news...")
    try:
        articles = get_security_news(api_key)
        
        print(f"Found {articles} articles.")
        if not articles:
            print("No articles found.")
            sys.exit(0)

        # Generate a post for the first article
        article = articles[0]
        print(f"Generating post for article: {article['title']}")
        
        generated_content = generate_content_from_article(article)
        filename, full_content = create_jekyll_post(article, generated_content)

        posts_dir = "_posts"
        os.makedirs(posts_dir, exist_ok=True)
        filepath = os.path.join(posts_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Successfully created post: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with NewsAPI: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
