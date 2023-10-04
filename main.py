import requests


def search_and_summarize(query):
    # Google Search API key and custom search engine ID
    api_key = 'AIzaSyD4wgD217rChlezK3d7asdQyE6Q21qPY_w'
    cx = 'c5a6a940d934a45a2'

    # Make a request to Google Search API
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}'
    response = requests.get(url)
    search_results = response.json().get('items', [])

    # Extract relevant information
    results_info = []
    for result in search_results[:5]:
        title = result.get('title', '')
        url = result.get('link', '')
        snippet = result.get('snippet', '')
        print(title);
        results_info.append(f"{title}\n{url}\n{snippet}\n\n")

    # Generate a summary
   
# Example usage
search_and_summarize("programming languages")

