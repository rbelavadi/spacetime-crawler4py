import json
from urllib.parse import urlparse
from collections import defaultdict

def question_one(unique_urls, line):
    # How many unique pages did you find?
    url = line['url']
    base_url = url.split('#')[0]
    unique_urls.add(base_url)

def question_two(longest_page, most_words, line):
    # What is the longest page 
    url = line['url']
    lenwords = len(line['tokens'])
    if lenwords > most_words:
        most_words = lenwords
        longest_page = url
    return longest_page, most_words

def question_three(line, word_count):
    # What are the 50 most common words 
    # in the entire set of pages
    stopwords = ["about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]
    words = line['tokens']
    for word in words:
        if len(word) == 1:
            continue
        if (word in stopwords):
            continue
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

def question_four(line, subdomain_pages):
    # How many subdomains did you find 
    # in the uci.edu domain?
    url = line['url']
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    if domain and domain.endswith("uci.edu"):
        subdomain = parsed_url.hostname
        subdomain_pages[subdomain].add(url)

def print_results():
    with open('saved_words.jsonl', 'r') as file:
        unique_urls = set()
        longest_page = ""
        most_words = 0
        word_count = {}
        subdomain_pages = defaultdict(set)
        
        for line in file:
            file = json.loads(line)
            question_one(unique_urls, file)
            longest_page, most_words = question_two(longest_page, most_words, file)
            question_three(file, word_count)
            question_four(file, subdomain_pages)
            
        top_50_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:50]
        total = 0
        for subdomain in subdomain_pages:
            total += len(subdomain_pages[subdomain])
    
    print(f"Question1: {len(unique_urls)} unique pages found.")
    print(f"Question2: {longest_page} ({most_words} words)")
    print("Question3:")
    for word, count in top_50_words:
        print(f"{word}: {count}")
    print(f"Question4: {total} subdomains found in uci.edu domain.")

if __name__ == "__main__":
    print_results()