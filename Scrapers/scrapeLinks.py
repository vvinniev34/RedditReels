from scrapeSafariPost import getContent
from datetime import date

  

if __name__ == "__main__":
    # Define the URL of the Reddit page you want to scrape
    today = date.today().strftime("%Y-%m-%d")

    filePath = f"redditPosts/{today}/links.txt"
    download_path = f"redditPosts/{today}/Texts"
    file = open(filePath, 'r')
    links = file.readlines()
    subreddit = "TIFU"
    count = 1
    for link in links:
        if link.strip():
            tryLink = "https://" + link
            path = download_path + '/' + subreddit
            if "reddit.com" in tryLink:
                # print(link)
                getContent(tryLink, path, subreddit, count)
                count += 1
            else:
                subreddit = link.strip()
                count = 1

