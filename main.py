import requests
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def search_and_summarize_all(query):
    # Google Search API key and custom search engine ID
    api_key = 'AIzaSyD4wgD217rChlezK3d7asdQyE6Q21qPY_w'
    cx = 'c5a6a940d934a45a2'

    # Make a request to Google Search API
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}'
    response = requests.get(url)
    search_results = response.json().get('items', [])

    # Extract information and fetch content from each page
    results_info = []
    for result in search_results[:5]:
        title = result.get('title', '')
        url = result.get('link', '')
        snippet = result.get('snippet', '')

        # Fetch the content of the page
        page_content = fetch_page_content(url)

        # Add title, URL, snippet, and content to the results_info
        results_info.append({
            'title': title,
            'url': url,
            'snippet': snippet,
            'content': page_content
        })

    # Generate a summary with titles as search queries and links as references
    full_summary = ''
    for result_info in results_info:
        full_summary += f"\n\n**Search Query: {result_info['title']}**\n"
        full_summary += f"Reference: [{result_info['title']}]({result_info['url']})\n\n"
        full_summary += f"Snippet: {result_info['snippet']}\n\n"
        full_summary += f"Content Summary: {generate_content_summary(result_info['url'])}\n"


    # Display the full summary
    print(full_summary)

def fetch_page_content(url):
    # Fetch the content of the page
    response = requests.get(url)
    page_content = response.text
    return page_content

def generate_content_summary(url):
    # Generate a summary of the content using LSA
    parser = HtmlParser.from_url(url, Tokenizer('english'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)  # You can adjust the number of sentences in the summary
    return ' '.join(str(sentence) for sentence in summary)

# Example usage
search_and_summarize_all("programming languages")
