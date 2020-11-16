import requests
import sys
if __name__ == '__main__':
    repo=str(sys.argv[1])
    url="https://cs-ej4104-fall-2020.github.io/"+repo.split("/")[1]
    data = requests.get(url)
    if data.status_code == 404:
        print("gh-pages url :"+url+" is not reachable.")
        print("possible causes :")
        print("1. github pages not enabled.")
        print("2. gh-pages branch does not contain valid index.html file")
        print("3. Make sure the chosen branch for gh-pages is gh-pages")
        print("Try building the code locally to see if index.html is properly generated.")
        sys.exit(1)
    else:
        print("URL reachable : OK")
