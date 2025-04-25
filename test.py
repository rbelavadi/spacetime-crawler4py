from urllib.parse import urlparse
import re


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False

        allowed = {
            "www.ics.uci.edu",
            "www.cs.uci.edu",
            "www.informatics.uci.edu",
            "www.stat.uci.edu",
            "www.today.uci.edu"
        }

        domain = parsed.netloc.lower()
        if not any(domain == d or domain.endswith("." + d) for d in allowed):
            return False

        if domain == "today.uci.edu" and not parsed.path.startswith("/department/information_computer_sciences/"):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()
        )

    except TypeError:
        print("TypeError for", url)
        return False

test_urls = [

    "http://www.ics.uci.edu",
    "https://www.cs.uci.edu/index.html",
    "http://vision.ics.uci.edu/about",
    "http://today.uci.edu/department/information_computer_sciences/events",
    "http://www.google.com",
    "http://engineering.uci.edu",
    "http://today.uci.edu/some/other/path",
    "http://www.ics.uci.edu/image.png",
    "http://www.cs.uci.edu/file.pdf",
    "ftp://www.ics.uci.edu"
]

for url in test_urls:
    print(f"{url} -> {is_valid(url)}")