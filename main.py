#TODO
#let users add/remove from keyLists
#let users get more info about each match (more context)
#let users toggle line #, indexes, etc
#give option to display when match found but in ignore list
#order lists depending on likelyhood of actaully endpoint
import re, requests
from urllib.parse import urljoin
underline= "\x1B[4m"
escape= "\x1B[0m"
#vars
contextLength=40 #the ammount of chars (on each side) returned in context around the match found (from keysList) in .js file 

def foundKeys(foundKeysList): # display keys found
    with open("ignoreKeysList.txt") as f:
        ignoreList = [line.strip().lower() for line in f if line.strip() and not line.startswith("#")]

    index=0
    for item in foundKeysList:
        matchText=item['context'].lower()
        if any(ignored in matchText for ignored in ignoreList): #skip ignored patterns in ignoreKeyList.txt
            continue

        index+=1
        print(f"\n{index}: [URL] {item['url']}")
        padding = " " * (len(str(index)) + 2)
        print(f"{padding}[Match] {item['match']}")

        if '\n' in item['context'] or item['line'] > 1: #only print line numbers if file is multi-line
            print(f"{padding}[Line #] {item['line']}")
        else:
            print(f"{padding}[Index] {item['index']}")    

        print(f"{padding}[Context] ...{(item['context'][:(item['context'].find(item['match']))]+underline+item['match']+escape+item['context'][(item['context'].find(item['match']))+len(item['match']):])}...")
    newC=(item['context'][:(item['context'].find(item['match']))]+underline+item['match']+escape+item['context'][(item['context'].find(item['match']))+len(item['match']):])
    

def check_js(urlList): #check each .js if contains a key
    with open("keysList.txt") as f:
        keysList=[line.strip() for line in f if line.strip() and not line.startswith("#")]

    pattern = re.compile(
        r"(?i)(" + "|".join(re.escape(k) for k in keysList) + r")"
    )

    foundKeysList=[]
    for url in urlList:
        try:
            response = requests.get(url,timeout=10)
            if response.status_code == 200:
                pageText = response.text
                for m in pattern.finditer(pageText):
                    #if .js sorted by lines
                    lineNumber=pageText.count('\n',0,m.start())+1
                    lineStart=pageText.rfind('\n',0,m.start())
                    lineEnd=pageText.find('\n',m.end())
                    if lineStart==-1:
                        lineStart=0
                    if lineEnd==-1:
                        lineEnd=len(pageText)
                    line=pageText[lineStart:lineEnd].strip()

                    if len(line)>200 or '\n' not in line:#if file is one long line
                        shortStart=max(0,m.start()-contextLength) #context 40 chars of found instance
                        shortEnd=min(len(pageText),m.end()+contextLength) #context +40 chars found instance
                        line= pageText[shortStart:shortEnd].strip()
                    context= line.replace('\n',' ') #put on one line

                    foundKeysList.append({
                        "url": url,
                        "line": lineNumber,
                        "match": m.group(0),
                        "context": context,
                        "index": m.start()
                    })
        except requests.RequestException:
            print(f'[!] Error fetching {url}')
            continue
    foundKeys(foundKeysList)


def get_js(url): #find .js files on valid pages' source code
    response = requests.get(url)
    if response.status_code == 200:
        sourceCode = response.text
        validMatch=re.compile(r'"([^"]*\.js)"') #find file name of .js files
        matches =validMatch.findall(sourceCode)

        #remove suburl
        filePathParent= r'\.\./'
        #remove ../ and replace with real url
        for i in range(len(matches)):
            indicies=[]
            for short in re.finditer(filePathParent, matches[i]):
                indicies.append(short.start())
            
            for appearance in indicies:
                matches[i]=urljoin(url,matches[i])
                    
        print(".js Files Found:",len(matches))
        return matches 
    else:
        print(f"Failed to retrieve page {response.status_code}")

def main():
    while True:
        url = input("URL to Scan: ")
        if "https://" not in url:
            url = "https://"+url 
        check_js(get_js(url))
main()

