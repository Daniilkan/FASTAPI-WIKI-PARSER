import requests
from bs4 import BeautifulSoup
import re

def parse_article(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    text = soup.find_all("p")
    summary = ""
    for p in text:
        summary += p.get_text()
    cleaned_text = re.sub(r'\[.*?\]', '', summary)
    cleaned_text = cleaned_text.replace('\n', '')
    return cleaned_text

def clean_urls(urls):
    cleaned_urls = []
    for url in urls:
        # Exclude URLs with unwanted query parameters
        if re.search(r"(action=|diff=|edit|preload|oldid)", url):
            continue
        if "wikipedia.org/" not in url:
            continue
        cleaned_urls.append(url)
    return cleaned_urls

def parse_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href.startswith('http'):
            links.append(href)
    return clean_urls(links)
