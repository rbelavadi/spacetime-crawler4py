import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
import json
import os
import PartA

def scraper(url, resp):
    init_jsonl()
    if resp.status != 200:
        return []

    if resp.raw_response is None:
        return []
    
    if is_low_info(resp.raw_response.content):
        return []

    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

# Initializes jsonl file (FIRST LINE OF JSONL FILE IS WORTHLESS)
def init_jsonl():
    if os.path.isfile("saved_words.jsonl"):
        return
    data = {
        "url": 'none.com',
        "tokens": [],
    }
    # Write to JSONL file
    with open("saved_words.jsonl", "w") as f:
        f.write(json.dumps(data) + "\n")

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

    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    links = set()
    
    text = soup.get_text(separator = " ", strip=True) # Gets all text
    tokens = PartA.tokenize(text) # Tokenize text into words (including ')
    
    data = {
        "url": resp.url,
        "tokens": tokens,
    }
    # Store dictionary in json lines file
    with open("saved_words.jsonl", "a") as file:
        file.write(json.dumps(data) + "\n")

    for tag in soup.find_all('a', href=True):
        href = tag['href']
        abs_href = urljoin(url, href)
        clean_href = urldefrag(abs_href)[0] 
        links.add(clean_href)
    return list(links)

# def merge_dict(dict1, dict2):
#     new = Counter(dict1) + Counter(dict2)
#     sorted_d = dict(sorted(new.items(), key=lambda item: item[1], reverse=True))
#     return sorted_d
    
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

        lower_query = parsed.query.lower()
        trap_keywords = ["sessionid=", "sort=", "tab_files=", "do=media", "do=diff", "eventdate=", "tribe-bar-date=",
        "do=edit", "rev=", "idx=", "ical=", "outlook-ical=", "view=", "action=", "controller="]

        lower_path = parsed.path.lower()
        if any(keyword in lower_query or keyword in lower_path for keyword in trap_keywords):
            return False
        
        if "/day/" in lower_path and re.search(r"\d{4}-\d{2}-\d{2}", lower_path):
            return False
        
        if re.search(r"/\d{4}-\d{2}$", parsed.path):
            return False

        if "events/list/page" in parsed.path and parsed.query:
            return False


        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4|mpg|mpeg|img"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|apk|war"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for", url)
        return False

def is_low_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(["script", "style", "meta", "noscript", "header", "footer"]):
        tag.decompose()

    text = soup.get_text(separator=' ')
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words = set(words)
    link_count = len(soup.find_all('a'))
    total_text_len = len(words)

    if total_text_len < 25 or len(unique_words) < 10:
        return True
    if link_count > 200 and total_text_len / (link_count + 1) < 1.5:
        return True
    return False