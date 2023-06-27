import requests
from bs4 import BeautifulSoup
import openai

#openai.api_key = "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"

def scrape_google_news(keyword, num_articles=18):
    url = f'https://news.google.com/rss/search?q={keyword}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    
    news_data = []
    for item in soup.find_all('item')[:num_articles]:
        news_item = {
            'title': item.title.text,
            'link': item.link.text,
            'source': item.source.text
        }
        news_data.append(news_item)
    
    return news_data

def scrape_bgoogle_news(keyword, num_articles=18):
    url = f'https://news.google.com/rss/search?q=negative%20news%20ticker%20{keyword}&hl=en-US&gl=US&ceid=US:en'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    
    news_data = []
    for item in soup.find_all('item')[:num_articles]:
        news_item = {
            'title': item.title.text,
            'link': item.link.text,
            'source': item.source.text
        }
        news_data.append(news_item)
    
    return news_data
    
def get_gpt4_response(model, messages):
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=0.5,
    max_tokens=14000,
    )
    return response.choices[0].message['content']

def apply_mosaic_theory_google(keyword,model):
    news_data = scrape_google_news(keyword)
    gpt4_output = get_gpt4_response(model, [
        {"role": "system", "content": "You are a hedge fund investment analyst."},
        {"role": "user", "content": f"Perform a mosaic analysis on {keyword} using the following news data: {news_data}"},
    ])

    # Extract summarized analysis and links from the GPT-4 output
    # Adjust this code as needed to extract the desired information from the GPT-4 output
    summarized_analysis = gpt4_output

    return {
        'analysis': summarized_analysis,
        'news_data': news_data,
    }

