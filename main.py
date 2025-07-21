import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def get_js(url):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser') #parses text
    scripts = soup.find_all('script', src=True) #finds all text with 'script' tag
    return [urljoin(url, tag['src']) for tag in scripts] #ignores inline


def fetch_js(urls):
    code_list = []
    for url in urls:
        try:
            resp = requests.get(url)
            code_list.append((url, resp.text))
        except Exception as e:
            print(f"Error fetching {url}: {e}")
    return code_list    

def scan(js_code_list):
    patterns = {
        "API Key": r'(?i)(api[_-]?key)[\s:=\'"]+[A-Za-z0-9\-_]{16,}',
        "JWT": r'eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+',
        "Token": r'(?i)(token)[\s:=\'"]+[A-Za-z0-9\-_\.]+'
        # "Base64": r'([A-Za-z0-9+/]{20,}={0,2})'
    }

    for url, code in js_code_list:
        print(f"\n Scanning {url}")
        for label, pattern in patterns.items():
            matches = re.findall(pattern, code)
            for m in matches:
                print(f"{label} found: {m[:60]}{'...' if len(m)>70 else ''}")

def main():
    url = input('URL to scan: ')
    js_urls = get_js(url)
    print(len(js_urls), "URLs found")
    js_code_list = fetch_js(js_urls)
    scan(js_code_list)
if __name__ == "__main__":
    main()