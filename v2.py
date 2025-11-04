import re, requests

def get_js(url): #find .js files on valid pages' source code
    response = requests.get(url)
    if response.status_code == 200:
        sourceCode = response.text
        validMatch=re.compile(r'"([^"]*\.js)"') #find file name of .js files
        matches =validMatch.findall(sourceCode)

        #remove suburl
        filePathParent= r'\.\./'
        pathUrl=url.split('/')
        #remove https:// from url
        pathUrl.pop(0)
        pathUrl.pop(0)
        
        for match in matches:
            indicies=[]
            for short in re.finditer(filePathParent, match):
                indicies.append(short.start())
                for appearance in indicies:
                    match=match[(appearance)+3:]
                print(match)
                    

        print(indicies,pathUrl)




        print("Javascript found:",len(matches))
        return matches 
    else:
        print(f"Failed to retrieve page {response.status_code}")
def main():
    while True:
        url = input("URL to Scan: ")
        if "https://" not in url:
            url = "https://"+url 
        print(get_js(url))
main()

