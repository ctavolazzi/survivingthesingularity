import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json

def is_valid_url(url):
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

def process_entry(entry):
    title = entry.title if 'title' in entry else 'No title'
    link = entry.link if 'link' in entry else 'No link'
    published = entry.published if 'published' in entry else 'No publish date'

    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
        headings = [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        valid_urls = [link.get('href') for link in soup.find_all('a') if is_valid_url(link.get('href'))]
        valid_image_urls = [img.get('src') for img in soup.find_all('img') if is_valid_url(img.get('src'))]

        entry_data = {
            'title': title,
            'link': link,
            'published': published,
            'paragraphs': paragraphs,
            'headings': headings,
            'valid_urls': valid_urls,
            'valid_image_urls': valid_image_urls
        }

        return entry_data

    except requests.exceptions.RequestException as e:
        print(f"Error accessing the link: {e}")
        return None

def get_news_feed(url):
    feed = feedparser.parse(url)
    entries_data = []

    for entry in feed.entries:
        entry_data = process_entry(entry)
        if entry_data:
            entries_data.append(entry_data)

    return entries_data

def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def display_entry(entry):
    print(f"Title: {entry['title']}")
    print(f"Link: {entry['link']}")
    print(f"Published: {entry['published']}")

    print("Paragraphs:")
    for paragraph in entry['paragraphs']:
        print(f"- {paragraph}")

    print("Headings:")
    for heading in entry['headings']:
        print(f"- {heading}")

    print("URLs:")
    for url in entry['valid_urls']:
        print(f"- {url}")

    print("Image URLs:")
    for image_url in entry['valid_image_urls']:
        print(f"- {image_url}")

    print("---")

def get_user_input():
    url = input("Enter a URL (or press Enter to use the default URL): ")
    if url.strip() == "":
        # url = "https://abcnews.go.com/abcnews/usheadlines"  # Default URL
        url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    return url

def main():
    url = get_user_input()

    print(f"Processing feed: {url}")
    entries_data = get_news_feed(url)

    if entries_data:
        save_to_json(entries_data, 'feed_data.json')

        # Load data from JSON file
        feed_data = load_from_json('feed_data.json')

        # Display entries
        print("\nEntries:")
        for entry in feed_data:
            display_entry(entry)
    else:
        print("No entries found in the feed.")

if __name__ == '__main__':
    main()