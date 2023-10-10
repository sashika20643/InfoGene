from flask import Flask, render_template, request
import requests
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

def fetch_page_content(url):
    response = requests.get(url)
    return response.text

def generate_content_summary(url):
    parser = HtmlParser.from_url(url, Tokenizer('english'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 10)  # You can adjust the number of sentences in the summary
    return ' '.join(str(sentence) for sentence in summary)

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
            
        })

    # Generate a summary with titles as search queries and links as references
    full_summary = ''
    for result_info in results_info:
        
        full_summary = "\n\nContent Summary: {}\n".format(generate_content_summary(result_info['url']).replace('\n', '<br>'))
        result_info['content']=full_summary 
    

    # Display the full summary
    print (full_summary)
    return results_info, full_summary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form['query']
    results_info, full_summary = search_and_summarize_all(query)
    return render_template('results.html', query=query, results_info=results_info, full_summary=full_summary)

if __name__ == '__main__':
    app.run(debug=True)
