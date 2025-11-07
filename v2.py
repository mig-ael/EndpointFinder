import re, requests
from urllib.parse import urljoin

def check_js(matches): #check each .js if contains a key

    #TODO: optimize searching
    with open("keysList.txt") as f:
        keysList=[line.strip() for line in f if line.strip() and not line.startswith("#")]
    keys=[]
    for match in matches:
        response = requests.get(match)
        if response.status_code == 200:
            pageText = response.text
            for key in keysList:
                validkey = re.compile(key)
                keys+=validkey.findall(pageText)

    print(keys)

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
                    
        print("Javascript found:",len(matches))
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

