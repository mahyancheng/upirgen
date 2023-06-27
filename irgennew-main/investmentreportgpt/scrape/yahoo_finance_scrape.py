import requests
from bs4 import BeautifulSoup
import openai

#openai.api_key = "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"

def scrape_yahoo_finance_news(keyword, num_articles=18):
    url = f'https://finance.yahoo.com/quote/{keyword}/news?p={keyword}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    news_data = []
    for item in soup.find_all('li', class_='js-stream-content')[:num_articles]:
        news_item = {
            'title': item.find('h3').text,
            'link': item.find('a')['href'],
            'source': 'Yahoo Finance'
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

def apply_mosaic_theory_yahoo_finance(keyword,model):
    news_data = scrape_yahoo_finance_news(keyword)
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
