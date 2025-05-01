import re
from urllib.parse import urlparse
import PartA
import json
from collections import Counter
import os

def scraper(url, resp):
    init_json()
    if resp.status != 200:
        return []

    if resp.raw_response is None:
        return []

    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

# Initializes json file
def init_json():
    if os.path.isfile("saved_words.json"):
        return
    data = {
        "largest": ['none.com', 0],
        "words": {}
    }
    # Write to JSON file
    with open("saved_words.json", "w") as f:
        json.dump(data, f, indent=4)

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content

    from bs4 import BeautifulSoup
    from urllib.parse import urljoin, urldefrag

    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    links = set()
    
    text = soup.get_text(separator = " ", strip=True) # Gets all text
    tokens = PartA.tokenize(text) # Tokenize text into words (including ')
    wordDict = PartA.computeWordFrequencies(tokens) # Compute word frequencies of all tokens
    
    # Load dictionary from file, update dictionary
    with open("saved_words.json", "r") as file: 
        prev = json.load(file)
        largest = prev['largest'][1]
        numwords = len(tokens)
        if largest < numwords:
            prev['largest'] = [resp.url, numwords]
        # prev = Counter(prev) + Counter(wordDict) # Add dictionaries together
        merged = merge_dict(prev['words'], wordDict)
        prev['words'] = dict(merged)
    
    # Store dictionary in json file
    file = open("saved_words.json", "w")
    json.dump(prev, file)
    file.close()
    
    for tag in soup.find_all('a', href=True):
        href = tag['href']
        abs_href = urljoin(url, href)
        clean_href = urldefrag(abs_href)[0] 
        links.add(clean_href)
    return list(links)

def merge_dict(dict1, dict2):
    new = Counter(dict1) + Counter(dict2)
    sorted_d = dict(sorted(new.items(), key=lambda item: item[1], reverse=True))
    return sorted_d
    
def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        #discuss whether we need "www."
        allowed = {
            "ics.uci.edu",
            "cs.uci.edu",
            "informatics.uci.edu",
            "stat.uci.edu",
            "today.uci.edu"
        }

        domain = parsed.netloc.lower()
        if not any(domain == d or domain.endswith("." + d) for d in allowed):
            return False

        if domain == "today.uci.edu" and not parsed.path.startswith("/department/information_computer_sciences/"):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4|img"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|apk|war"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for", url)
        return False
